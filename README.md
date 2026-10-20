# Story Map

Story Map is a reusable Copilot skill that turns a supplied book into a spoiler-aware, navigable HTML reading companion. It analyzes chapters in sequence, preserves the boundary between chapter-level observations and whole-work insights, and adapts its output to novels, collections, and nonfiction.

## Use the skill

Open this repository (or another repository containing the skill) as a VS Code workspace, then invoke `/story-map` in Copilot Chat with an accessible book file or attached text. For example:

```text
/story-map

Analyze the book at "C:\Users\YourName\Books\Example Novel.epub".
Output folder: Use the default repository-root folder named after the book.
Temporary files: Delete this run's .temp folder after validating the finished pages.
Do not modify or move the original book file.
```

The skill and its complete invocation guidance are in [`SKILL.md`](.github/skills/story-map/SKILL.md). Provide an accessible source path or attach/paste the book; the skill will not search unrelated folders for it.

## What it creates

The output route depends on the book's structure:

- **One continuous novel:** a spoiler-free home page, one analysis page per chapter, and a spoiler-marked whole-book analysis.
- **A volume containing multiple novels:** a catalog and a separate chapter map and whole-book analysis for each novel, without a volume-wide plot summary.
- **Standalone stories presented as chapters:** a navigation page and a separate analysis page for each story, without a combined story-cycle analysis.

By default, output goes in a book-named folder at the repository root. The source is copied before processing; run-specific temporary work is kept in that output folder's `.temp` directory and removed after validation unless retention is requested.

## EPUB support

The optional EPUB extractor uses only Python's standard library. It processes readable, unencrypted EPUBs locally; it does not upload files or bypass DRM. See the [EPUB extraction guide](.github/skills/story-map/scripts/README.md).

Run its tests from the repository root:

```powershell
python .github\skills\story-map\scripts\test_extract_epub.py
```

## License

This project is available under the [MIT License](LICENSE).
