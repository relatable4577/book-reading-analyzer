---
name: story-map
description: "Analyze books, chapters, and story collections with genre-aware, spoiler-safe reading companions. Create navigable multi-page HTML maps, track characters, events, themes, and open threads, connect chapters, explain cultural context, and synthesize each work. Use when analyzing a novel, anthology, omnibus, memoir, or other book."
---

# Story Map

Turn a book into a static, navigable HTML reading companion. Choose the output route based on the narrative structure: a continuous novel gets chapter pages and a spoiler-marked book analysis; a volume containing multiple novels gets a separate chapter-by-chapter map and book analysis for each novel but no volume-wide story summary; a volume whose chapters are standalone stories gets one analysis page per chapter/story and no combined book analysis. Chapter pages never use information from later chapters; later material appears only in the relevant whole-work analysis when that analysis route applies.

## When to Use
- The user provides a book, excerpt, anthology, omnibus, or chapters and wants genre-aware chapter/work and whole-work analysis.
- The user wants a reading companion, story map, or a structured basis for planning a film adaptation.

## How to Invoke

In VS Code, enter this in the **Copilot Chat input**—not in Windows Command Prompt or PowerShell. Invoke the skill with `/story-map`, then include the book source and any preferences in the same chat message. Attach the book instead of giving a path if it is not accessible from the current workspace.

Complete example:

```text
/story-map

Analyze the book at "C:\Users\YourName\Books\Example Novel.epub".

Known details (if helpful):
- Title: Example Novel
- Author: Example Author
- Edition/translation: Unknown

Output folder: Use the default repository-root folder named after the book.
Temporary files: Delete this run's .temp folder after validating the finished pages.
Do not modify or move the original book file. First determine whether this is one continuous novel, a volume containing multiple novels, or a volume whose chapters are standalone stories, and follow the matching output route.
```

If attaching/pasting the book instead of using a path, replace the source line with `Analyze the attached book` or `Analyze the text below`. To retain working files, change the temporary-files line to `Retain this run's temporary files and tell me where they are`.

The source file/text is required unless already attached or provided in the conversation. The title, author, edition, and translation may be supplied by the user or identified from the source; the user does not need to classify the material in advance. The output path and temporary-file retention are optional. If no output path is specified, use `<repository-root>/<book-slug>/`; temporary working files go under that folder's `.temp/<run-id>/`.

Expected deliverable depends on the material:
- **One continuous novel:** spoiler-free home, one page per chapter, and a spoiler-marked whole-book analysis.
- **A volume containing multiple novels:** a collection catalog plus a separate home, chapter pages, and whole-book analysis for each included novel; no combined volume-wide story summary.
- **Standalone stories presented as chapters:** a navigation-only landing page and one analysis page per chapter/story; no additional whole-book or story-cycle analysis.

## Principles
- **Book first.** Base story analysis on the provided text. Consult open, reliable sources only when something is unclear or an outside perspective helps (edition metadata, real-world events, cultural references, spoiler-free plot summary). Cite every external claim that informs the output.
- **Separate evidence from interpretation.** Distinguish what the text directly supports, what external sources verify, and what is interpretation. Qualify plausible but unconfirmed readings; never present them as fact.
- **Cite the book.** Reference chapter numbers for events and cross-chapter links. Use short quotations selectively, only when they add clarity. Never guess missing content.
- **Preserve spoiler boundaries.** A chapter page may use only that chapter and prior chapters in the same work. Do not import reveals from later chapters or later books in a series. The whole-work analysis may use the complete supplied work, not unsupplied sequels.
- **Establish continuity from evidence.** Chapter labels, repeated names, settings, or motifs do not by themselves prove that sections belong to one continuous story or that characters with the same name are the same person. Treat disconnected, self-contained stories as separate works; carry identity and plot continuity across them only when the text supports it.
- **Concise but substantive.** Explain key developments and support interpretations without retelling every scene. Expand for dense chapters or on request.
- **Adaptation-friendly, not a screenplay.** When useful, add a clearly labelled, optional adaptation lens noting causal event chains, major turns, stakes, character goals, visually significant settings or motifs, and moments that rely on internal thought or narration. Keep this separate from literary analysis; do not write scenes, dialogue, or a screenplay unless asked.
- **Age and content advisories.** Include a visible age/content advisory when an official rating or mature-content concern is known. Distinguish a verified official age classification (including its rating system/source) from a descriptive content advisory; do not invent an official "18+" rating. Keep advisories concise, non-graphic, and limited to relevant themes. An advisory informs readers but does not guarantee that every model can process the material or override any model's content limits.
- **Respect model limits.** Do not bypass, disguise, or transform restricted source material to evade the active model's policies. If the material cannot be processed, explain the limitation and offer a permitted high-level alternative where possible.
- **Safe HTML output.** Treat all book text, quotations, and research as plain text and HTML-escape it before inserting it into a template. Add only deliberate, minimal markup for structure (such as paragraphs, lists, blockquotes, and cited links). Never insert scripts, event-handler attributes, or untrusted HTML.

## Intake and analysis routing

Before analyzing, use the concise decision checklist in [analysis-workflow.md](./references/analysis-workflow.md). If the user has not attached/provided the book text or identified an accessible source path, ask for the book file's path or for the file/text to be provided; do not guess a location or search unrelated directories. If the supplied path is inaccessible in the current environment, explain that and ask the user to attach the file or provide the text. The output directory is optional; use the documented default unless the user specifies another path. Temporary-file retention is also optional: remove this run's temporary files by default, and retain them only if the user explicitly requests this at the start. Do not expose private chain-of-thought; report only decisions, findings, evidence, and uncertainty. Classify the supplied material, identify its work boundaries and genres, choose the matching [genre lens](./references/genre-lenses/README.md), and select the single-work or collection workflow. Do not infer narrative continuity or character identity from repeated names alone. Treat the user's supplied text as authoritative for literary analysis.

## Procedure

### 1. Identify the book and verify metadata
1. Confirm the source material: use an attached file, pasted text, or an explicitly provided accessible file path. If none is available, ask the user for the book's path or to attach/paste the material before proceeding. Do not assume the book is in the workspace or search the user's filesystem without a supplied location. Identify the title and author; note the edition, translation, or format if the user provided it or the file establishes it.
2. Use open, reliable sources to check the expected chapter count and chapter titles. Verify pagination or length only when useful; page counts vary by edition and do not determine story coverage. Novel editions usually tell the same story, so do not over-investigate edition differences.
3. Treat the provided text as authoritative for analysis. If the edition is unknown, metadata conflicts, or chapter divisions differ, briefly state the uncertainty and proceed without blocking. Compare the expected structure with chapters provided; record available, missing, or skipped chapters. Never infer unseen content.
4. Record any official age classification only when it is known and verifiable; otherwise use a neutral content advisory for relevant mature themes, or say no rating was verified. Do not infer an official rating from the book's themes alone.
5. For collections/omnibuses, verify the volume contents and each included work where possible. Apply [collections.md](./references/collections.md); do not assume that the physical volume is one narrative.
6. If the user supplies an EPUB, use the optional local extraction/review procedure in [scripts/README.md](./scripts/README.md) before analysis. Parse structure locally first, then have the active model review its metadata and bounded boundary excerpts; do not upload the EPUB or assume spine items are chapters.

### 2. Set up output and working files
1. Choose a final output folder (default `<repository-root>/<book-slug>/`, unless the user specifies another path). Keep generated book folders at the repository root, outside `.github/skills/story-map/`.
2. Create a unique run folder at `<output>/.temp/<run-id>/` for working files. Stage a copy of the supplied book there (never move, modify, or overwrite the original); save pasted text there as a source file. Put EPUB extraction output and JSON context/state under this run folder, for example `.temp/<run-id>/source/`, `.temp/<run-id>/epub-extracted/`, and `.temp/<run-id>/context/`.
3. By default, delete only the exact run folder created for this analysis after the final HTML output has been validated. If the user asks at the start to retain temporary files, preserve that run folder and report its path. Never delete a pre-existing `.temp` folder, another run's files, or any path not created by this run. If a unique run folder cannot be created safely, stop and ask the user how to proceed.
4. Copy [assets/](./templates/assets/) (`story-map.css`, `theme.js`) into `<output>/assets/`.
5. Select exactly one route from [analysis-workflow.md](./references/analysis-workflow.md) and [collections.md](./references/collections.md): (1) a continuous novel gets `index.html`, one `chapter.html` per chapter, and `book-analysis.html`; (2) a volume containing multiple novels gets a collection landing page plus a separate complete map (`index.html`, chapter pages, and `book-analysis.html`) for each novel, with no volume-wide story summary; (3) a volume whose chapters are standalone stories gets a navigation-only landing page and one `chapter.html` per chapter/story, with no story-cycle or book-wide analysis page. For an unchaptered standalone work, use `index.html` and `work-analysis.html`.
6. Keep `book-context.json`, `chapter-NNN.json`, and `collection.json` working records under `.temp/<run-id>/context/`, using the templates in `templates/context/`. Do not place working JSON or extracted source text in the final HTML output unless the user explicitly asks for those files to be delivered. See [context-json.md](./references/context-json.md) for efficient handoff and [placeholders.md](./references/placeholders.md) for HTML fields.
7. Name chapter HTML files consistently, such as `chapter-001.html`, and keep all links consistent. For stories without chapters, create one work-level analysis page; do not invent chapter divisions.
8. Fill every `[[PLACEHOLDER]]`, remove unused optional sections/placeholders, and omit irrelevant genre lenses. Templates are starting points; add a section only when useful, documenting new placeholders.

### 3. Maintain compact continuity state
For a continuous novel, analyze chapters in order and keep concise cumulative notes in that novel's JSON context under the run's `.temp/<run-id>/context/`. For a multi-novel volume, maintain a separate context for each novel. For standalone stories presented as chapters, keep each chapter/story's context separate; do not carry characters, events, themes, or open threads across stories based only on shared names or motifs. Carry a cross-story link only when the text supports it, and label uncertainty. At each new chapter, load only relevant context, not every previous analysis or the full book again. Store no full chapter text in JSON. Update affected records/pages when the user supplies corrections and mark missing/skipped units as gaps.

### 4. Analyze each chapter or work
For chapter pages in a continuous novel, use only that chapter and earlier chapters of the same work (and no later series volumes). For standalone-story chapters, analyze only that story; do not import characters or events from other stories based on repeated names. For a work without chapters, analyze the supplied work as a whole and mark the page as containing spoilers. Cover, when relevant:
- Summary, characters and interactions, character development
- Events, conflicts, and the chapter's turning point
- Connections to earlier chapters in the same continuous narrative, citing the chapter number of the past event; for standalone-story chapters, do not assume cross-story connections
- Setting, tone and mood, symbols and motifs, narrative techniques, point of view, and pacing
- Cultural references and real-world events, with a brief explanation so readers understand the context (state confidence; separate confirmed context from possible allusions)
- The ending (resolution or cliffhanger) and threads left open
- Evidence and notes

**Event names:** keep any name the book or common usage already gives an event (for example "The Purple Wedding"). Otherwise coin a short descriptive label, sensible or lightly playful, and mark it as coined for this analysis.

**External context and citations:** consult open sources only when needed to resolve uncertainty or add useful perspective. Prefer primary sources, publishers, libraries, and reputable reference works. Place a descriptive source link next to the relevant context; also list sources in the page's sources/notes area with publisher or site, page title, URL, and access date when available. Cite only sources that informed a claim; do not imply a source verifies more than it does.

For genre-specific questions, load only applicable guides from [genre-lenses/](./references/genre-lenses/README.md). Combine lenses for cross-genre works; never let genre expectations override textual evidence or the chapter spoiler boundary.

### 5. Write the landing page — no spoilers
For route (1), include title, author, edition and coverage, chapter count and available length details, a spoiler-free plot summary (open sources allowed; cite sources in `PLOT_SUMMARY_SOURCES`), the age/content advisory, and the chapter list. Keep the summary to premise and setup; exclude twists, deaths, and ending revelations. For route (2), the volume landing page is a catalog of included novels only; each novel's own home page follows route (1), and the volume page must not summarize or synthesize their plots. For route (3), use the landing page only for volume metadata, coverage, and chapter/story navigation; omit a volume plot summary, whole-book analysis callout, and any claim that separate stories form one narrative.

### 6. Write whole-work analysis only when the route calls for it
For route (1), after the final available chapter, synthesize across the continuous novel: character arcs, themes and final message, plot structure and causality, foreshadowing, open threads and payoffs, evolving symbolism, narrative choices and consistency, relationship dynamics, and resolution with alternative readings. For route (2), do this separately for each included novel, based only on the supplied version and coverage. If a novel is incomplete, say so and avoid conclusions that depend on unseen chapters. Keep the spoiler warning. Add the optional, clearly labelled adaptation lens when useful. For route (3), do not create a whole-book/story-cycle analysis; each chapter page analyzes only its standalone story, and no combined character arc or ending is inferred.

For collection behavior, follow [collections.md](./references/collections.md). Do not create a volume-wide plot synthesis for routes (2) or (3).

### 7. Validate
- Open the pages and confirm each internal link resolves (home, chapter, previous/next, whole-book analysis, assets).
- Confirm no `[[...]]` placeholders remain.
- Confirm the home page contains no spoilers and each chapter page has no information from later chapters.
- Confirm the theme toggle works on every page.
- Tell the user where the output is and what coverage gaps or uncertainties remain.
