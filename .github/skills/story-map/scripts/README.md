# EPUB extraction

`extract_epub.py` uses only Python's standard library. It reads the EPUB locally; it does not upload the file, call an AI service, or bypass DRM. When using it as part of the story-map workflow, point it at the staged copy of the user's EPUB and place its output under the current run's `.temp/<run-id>/` directory. Never modify or extract over the original book file.

```powershell
python .github\skills\story-map\scripts\extract_epub.py "story-maps\book-slug\.temp\run-id\source\book.epub" "story-maps\book-slug\.temp\run-id\epub-extracted"
```

The output directory must be new or empty. Use a unique run directory and keep its extracted text temporary; by default, the story-map workflow removes only that run directory after validating final HTML, unless the user asked to retain temporary files. The script creates:

- `manifest.json` — EPUB metadata, navigation/TOC, spine reading order, headings, short start/end excerpts, extraction status, and warnings.
- `sections\section-NNNN.txt` — cleaned text from each readable XHTML/HTML spine resource, in reading order.

Spine resources are **candidate sections, not guaranteed chapters**. A single XHTML item may contain several chapters, and a chapter may span multiple items. The script preserves the source order and avoids guessing those semantic boundaries.

## Recommended AI-assisted review

1. Run extraction locally.
2. Inspect `manifest.json` first. Use title/author/language metadata, TOC entries, spine order, headings, section lengths, and short boundary excerpts to propose candidate work/chapter groupings.
3. Classify each candidate as story text, supporting material (for example foreword, notes, glossary, or appendix), navigation/boilerplate, or uncertain. Do not automatically discard supporting material; retain it for selective use when relevant.
4. For ambiguous boundaries or inclusion decisions, inspect the corresponding extracted text around the proposed cut. Ask the model to confirm whether the previous section ends and the next begins as intended. The model must not certify a boundary from metadata alone if the boundary text is needed.
5. Compare the proposal against TOC and spine order, check for missing, duplicate, empty, unexpectedly short/long, or out-of-order sections, and preserve unresolved cases as review flags. Do not silently edit or drop extracted text.
6. Once boundaries are approved, analyze one chapter at a time and maintain the compact context JSON described in [context-json.md](../references/context-json.md).

The model is the semantic reviewer, not a separate extraction dependency: no AI API key or additional package is needed. EPUB parsing and mechanical checks are deterministic local work; boundary interpretation and content classification use the active assistant model, with user review for unresolved cases. Don't send the full EPUB or all extracted chapters at once when a compact manifest and targeted excerpts will suffice.

The extractor handles readable, unencrypted EPUB ZIP containers. If a file is DRM-protected, malformed, or uses unsupported content, report the limitation and ask for an accessible copy or user-provided text; do not attempt to circumvent protection.

## Tests

Run the standard-library tests from the repository root:

```powershell
python .github\skills\story-map\scripts\test_extract_epub.py
```
