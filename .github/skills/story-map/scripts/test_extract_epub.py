import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from extract_epub import extract_epub


class ExtractEpubTests(unittest.TestCase):
    def make_epub(self, root: Path) -> Path:
        epub = root / "sample.epub"
        with zipfile.ZipFile(epub, "w") as archive:
            archive.writestr(
                "META-INF/container.xml",
                """<?xml version="1.0"?>
                <container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
                  <rootfiles><rootfile full-path="OPS/package.opf"/></rootfiles>
                </container>""",
            )
            archive.writestr(
                "OPS/package.opf",
                """<?xml version="1.0"?>
                <package xmlns="http://www.idpf.org/2007/opf" version="3.0">
                  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
                    <dc:title>Sample Book</dc:title>
                    <dc:creator>Example Author</dc:creator>
                    <dc:language>en</dc:language>
                    <dc:identifier>sample-id</dc:identifier>
                  </metadata>
                  <manifest>
                    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
                    <item id="c1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
                    <item id="c2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
                  </manifest>
                  <spine>
                    <itemref idref="c1"/>
                    <itemref idref="c2"/>
                  </spine>
                </package>""",
            )
            archive.writestr(
                "OPS/nav.xhtml",
                """<html><body><nav epub:type="toc">
                  <ol><li><a href="chapter1.xhtml">First</a></li>
                  <li><a href="chapter2.xhtml">Second</a></li></ol>
                </nav></body></html>""",
            )
            archive.writestr(
                "OPS/chapter1.xhtml",
                """<html><head><title>First</title><style>.x{}</style></head><body>
                  <h1 id="one">Chapter One</h1><p>Hello <em>there</em>.</p>
                  <script>not book text</script><p>End of first.</p>
                </body></html>""",
            )
            archive.writestr(
                "OPS/chapter2.xhtml",
                """<html><body><h2>Chapter Two</h2><p>Second chapter text.</p></body></html>""",
            )
        return epub

    def test_extracts_spine_in_order_and_writes_review_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            epub = self.make_epub(root)
            output = root / "out"
            result = extract_epub(epub, output)

            self.assertEqual(result["metadata"]["title"], "Sample Book")
            self.assertEqual(result["metadata"]["creators"], ["Example Author"])
            self.assertEqual(result["reading_order"], ["section-0001", "section-0002"])
            self.assertEqual(result["sections"][0]["toc_entries"][0]["title"], "First")
            text = (output / "sections" / "section-0001.txt").read_text(encoding="utf-8")
            self.assertIn("Chapter One", text)
            self.assertIn("Hello there.", text)
            self.assertNotIn("not book text", text)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["review_guidance"]["status"], "pending_ai_review")

    def test_refuses_nonempty_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            epub = self.make_epub(root)
            output = root / "out"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not empty"):
                extract_epub(epub, output)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_rejects_invalid_epub(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            invalid = root / "not-an-epub.epub"
            invalid.write_text("not a zip", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Not a valid EPUB"):
                extract_epub(invalid, root / "out")


if __name__ == "__main__":
    unittest.main()
