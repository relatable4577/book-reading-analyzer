#!/usr/bin/env python3
"""Extract EPUB reading-order sections and create an AI boundary-review manifest."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


MAX_REVIEW_CHARS = 240
BLOCK_TAGS = {
    "address", "article", "blockquote", "br", "dd", "div", "dt", "figcaption",
    "h1", "h2", "h3", "h4", "h5", "h6", "li", "p", "pre", "section", "tr",
}
SKIP_TAGS = {"head", "script", "style", "svg"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def safe_archive_path(base: str, href: str) -> str:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        raise ValueError(f"External resource is not allowed in EPUB path: {href}")
    decoded = unquote(parsed.path)
    joined = posixpath.normpath(posixpath.join(base, decoded))
    if joined == ".." or joined.startswith("../") or joined.startswith("/"):
        raise ValueError(f"EPUB path escapes archive root: {href}")
    return joined


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.headings: list[dict[str, str]] = []
        self._skip_depth = 0
        self._heading_tag: str | None = None
        self._heading_id = ""
        self._heading_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = dict(attrs)
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        if self._skip_depth:
            return
        if tag in BLOCK_TAGS:
            self._newline()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = tag
            self._heading_id = values.get("id") or values.get("name") or ""
            self._heading_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if self._heading_tag == tag:
            title = " ".join("".join(self._heading_parts).split())
            if title:
                self.headings.append({"level": tag, "id": self._heading_id, "text": title})
            self._heading_tag = None
            self._heading_id = ""
            self._heading_parts = []
        if tag in BLOCK_TAGS:
            self._newline()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.replace("\xa0", " ")
        if self._heading_tag:
            self._heading_parts.append(text)
        if text.strip():
            self.parts.append(text)

    def _newline(self) -> None:
        if self.parts and self.parts[-1] != "\n":
            self.parts.append("\n")

    def text(self) -> str:
        joined = "".join(self.parts)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in joined.splitlines()]
        return "\n".join(line for line in lines if line).strip()


class NavigationParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[dict[str, str]] = []
        self._link: dict[str, str] | None = None
        self._depth = 0
        self._in_nav = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag.lower() == "nav":
            nav_type = (values.get("epub:type") or values.get("type") or "").lower()
            self._in_nav = "toc" in nav_type.split()
        if self._in_nav and tag.lower() == "a":
            self._link = {"href": values.get("href") or "", "title": ""}
            self._depth = 1
        elif self._link is not None:
            self._depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._link is None:
            if tag.lower() == "nav":
                self._in_nav = False
            return
        self._depth -= 1
        if tag.lower() == "a" and self._depth <= 0:
            self._link["title"] = " ".join(self._link["title"].split())
            self.entries.append(self._link)
            self._link = None

    def handle_data(self, data: str) -> None:
        if self._link is not None:
            self._link["title"] += data


def parse_xml(data: bytes, description: str) -> ElementTree.Element:
    try:
        return ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise ValueError(f"Invalid XML in {description}: {exc}") from exc


def read_container(archive: zipfile.ZipFile) -> str:
    try:
        root = parse_xml(archive.read("META-INF/container.xml"), "META-INF/container.xml")
    except KeyError as exc:
        raise ValueError("EPUB is missing META-INF/container.xml") from exc
    for element in root.iter():
        if local_name(element.tag) == "rootfile":
            path = element.attrib.get("full-path")
            if path:
                return safe_archive_path("", path)
    raise ValueError("EPUB container does not identify an OPF package document")


def extract_epub(epub_path: Path, output_dir: Path) -> dict[str, Any]:
    if not zipfile.is_zipfile(epub_path):
        raise ValueError(f"Not a valid EPUB/ZIP archive: {epub_path}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"Output directory is not empty: {output_dir}")

    with zipfile.ZipFile(epub_path) as archive:
        names = set(archive.namelist())
        opf_path = read_container(archive)
        if opf_path not in names:
            raise ValueError(f"OPF package document not found in archive: {opf_path}")
        package = parse_xml(archive.read(opf_path), opf_path)
        opf_dir = posixpath.dirname(opf_path)

        metadata: dict[str, Any] = {"title": "", "creators": [], "language": "", "identifier": ""}
        manifest: dict[str, dict[str, str]] = {}
        spine: list[dict[str, str]] = []
        nav_href = ""
        ncx_href = ""

        for element in package.iter():
            name = local_name(element.tag)
            if name in {"title", "creator", "language", "identifier"}:
                value = " ".join("".join(element.itertext()).split())
                if not value:
                    continue
                if name == "creator":
                    metadata["creators"].append(value)
                elif not metadata[name]:
                    metadata[name] = value
            elif name == "item":
                item_id = element.attrib.get("id", "")
                href = element.attrib.get("href", "")
                if not item_id or not href:
                    continue
                path = safe_archive_path(opf_dir, href)
                properties = element.attrib.get("properties", "")
                media_type = element.attrib.get("media-type", "")
                manifest[item_id] = {
                    "href": href,
                    "path": path,
                    "media_type": media_type,
                    "properties": properties,
                }
                if "nav" in properties.split():
                    nav_href = path
                if media_type == "application/x-dtbncx+xml":
                    ncx_href = path
            elif name == "itemref":
                idref = element.attrib.get("idref", "")
                if idref:
                    spine.append({"idref": idref, "linear": element.attrib.get("linear", "yes")})

        if not spine:
            raise ValueError("EPUB package has no readable spine entries")

        nav_entries: list[dict[str, str]] = []
        if nav_href and nav_href in names:
            parser = NavigationParser()
            parser.feed(archive.read(nav_href).decode("utf-8", errors="replace"))
            nav_entries = parser.entries
        elif ncx_href and ncx_href in names:
            ncx = parse_xml(archive.read(ncx_href), ncx_href)
            for point in ncx.iter():
                if local_name(point.tag) != "navpoint":
                    continue
                label = ""
                target = ""
                for child in point.iter():
                    if local_name(child.tag) == "text" and not label:
                        label = " ".join("".join(child.itertext()).split())
                    elif local_name(child.tag) == "content":
                        target = child.attrib.get("src", "")
                if target:
                    nav_entries.append({"href": target, "title": label})

        output_dir.mkdir(parents=True, exist_ok=True)
        sections_dir = output_dir / "sections"
        sections_dir.mkdir()
        sections: list[dict[str, Any]] = []
        for ordinal, itemref in enumerate(spine, start=1):
            item = manifest.get(itemref["idref"])
            if item is None:
                sections.append({
                    "section_id": f"section-{ordinal:04d}",
                    "spine_idref": itemref["idref"],
                    "linear": itemref["linear"],
                    "status": "missing_manifest_item",
                    "warnings": ["Spine reference has no manifest item."],
                })
                continue
            if item["path"] not in names:
                sections.append({
                    "section_id": f"section-{ordinal:04d}",
                    "spine_idref": itemref["idref"],
                    "href": item["href"],
                    "linear": itemref["linear"],
                    "status": "missing_resource",
                    "warnings": ["Manifest resource is absent from the archive."],
                })
                continue
            if "nav" in item["properties"].split():
                continue
            if item["media_type"] not in {"application/xhtml+xml", "text/html"} and not item["path"].lower().endswith((".xhtml", ".html", ".htm")):
                continue

            extractor = TextExtractor()
            try:
                extractor.feed(archive.read(item["path"]).decode("utf-8", errors="replace"))
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Could not parse EPUB content resource {item['path']}: {exc}") from exc
            text = extractor.text()
            section_id = f"section-{ordinal:04d}"
            filename = f"{section_id}.txt"
            (sections_dir / filename).write_text(text + ("\n" if text else ""), encoding="utf-8")
            review_headings = [
                {"level": heading["level"], "id": heading["id"], "text": heading["text"][:160]}
                for heading in extractor.headings[:30]
            ]
            if len(extractor.headings) > 30:
                warnings = [f"Only the first 30 of {len(extractor.headings)} headings are in the review manifest."]
            else:
                warnings = []
            toc_matches = [
                entry for entry in nav_entries
                if unquote(urlsplit(entry["href"]).path).endswith(item["href"].split("#", 1)[0])
                or unquote(urlsplit(entry["href"]).path).endswith(posixpath.basename(item["path"]))
            ]
            if not text:
                warnings.append("No readable text extracted.")
            if len(text) < 300:
                warnings.append("Very short section; confirm whether it is front/back matter or an incomplete extraction.")
            sections.append({
                "section_id": section_id,
                "spine_idref": itemref["idref"],
                "href": item["href"],
                "file": f"sections/{filename}",
                "linear": itemref["linear"],
                "status": "extracted",
                "classification": "pending_ai_review",
                "toc_entries": toc_matches,
                "headings": review_headings,
                "character_count": len(text),
                "start_excerpt": text[:MAX_REVIEW_CHARS],
                "end_excerpt": text[-MAX_REVIEW_CHARS:],
                "warnings": warnings,
            })

        manifest_data = {
            "schema_version": "1.0",
            "source_file": epub_path.name,
            "metadata": metadata,
            "reading_order": [section["section_id"] for section in sections],
            "toc": nav_entries,
            "sections": sections,
            "review_guidance": {
                "status": "pending_ai_review",
                "note": "Spine resources are candidate sections, not guaranteed chapters. Review TOC, headings, boundary excerpts, and flagged sections before grouping or excluding content.",
            },
        }
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return manifest_data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract EPUB spine text and create a compact boundary-review manifest."
    )
    parser.add_argument("epub", type=Path, help="Input EPUB file")
    parser.add_argument("output_dir", type=Path, help="New or empty output directory")
    args = parser.parse_args()

    try:
        manifest = extract_epub(args.epub, args.output_dir)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
        print(f"EPUB extraction failed: {exc}", file=sys.stderr)
        return 1

    extracted = sum(section.get("status") == "extracted" for section in manifest["sections"])
    warnings = sum(bool(section.get("warnings")) for section in manifest["sections"])
    print(f"Extracted {extracted} reading-order sections to {args.output_dir}")
    print(f"Boundary review required; {warnings} section(s) have extraction warnings.")
    print(f"Review metadata and excerpts in {args.output_dir / 'manifest.json'} before analysis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
