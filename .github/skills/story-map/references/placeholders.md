# Template placeholders

Replace every `[[PLACEHOLDER]]` in the generated pages. Treat replacement values as plain text and HTML-escape them by default. Only add deliberate, minimal markup for semantic structure (paragraphs, lists, blockquotes, and links). Never insert scripts, event-handler attributes, or untrusted HTML. When adding a new placeholder, document it and provide a matching section in the relevant template.

## `index.html` (spoiler-free)

| Placeholder | Content |
|---|---|
| `BOOK_TITLE`, `AUTHOR`, `EDITION` | Verified book details; use a concise note if edition is unknown |
| `COVERAGE_SUMMARY` | Short coverage statement, such as "Chapters 1–12 of 30" |
| `UNIT_COUNT_LABEL`, `UNITS_ANALYZED_LABEL` | Usually "Chapters"; for a work without chapters use an appropriate unit label |
| `EXPECTED_UNIT_COUNT`, `ANALYZED_UNITS` | Expected/analyzed chapters, sections, or work units; use "1" and "1" for a fully analyzed unchaptered work |
| `UNIT_LIST_HEADING` | Usually "Chapters"; use "Story" or "Work" if the work has no chapter divisions |
| `BOOK_LENGTH_AND_FORMAT` | Page or length details, when useful; explicitly edition-specific |
| `COVERAGE_NOTES` | Missing or skipped chapters, chapter-division differences, or uncertain metadata |
| `SPOILER_FREE_PLOT_SUMMARY` | Premise and setup only; no twists, deaths, or ending |
| `PLOT_SUMMARY_SOURCES` | Descriptive links for sources informing the summary (publisher/site, title, URL; access date when available) |
| `AGE_AND_CONTENT_ADVISORY` | Verified official age rating and rating system/source when available; otherwise a concise, non-graphic advisory for relevant mature themes. Never infer an official rating. |
| `CHAPTER_LIST_ITEMS` | One `<li>` per chapter/section, or a single link to the work analysis if unchaptered; built from the `chapter-list-item-template` template (then remove the `<template>` element) |
| `ANALYSIS_PAGE_FILE`, `ANALYSIS_PAGE_LABEL` | Whole-work analysis filename (usually `book-analysis.html` or `work-analysis.html`) and link label; omit the analysis callout for standalone-stories-as-chapters route |

Per list item: `CHAPTER_FILE`, `CHAPTER_NUMBER`, `CHAPTER_TITLE`, `CHAPTER_PAGE_RANGE_OR_LENGTH` for chaptered works; for an unchaptered work, use `CHAPTER_FILE`=`work-analysis.html`, `UNIT_DISPLAY_LABEL`=`Full work`, `UNIT_TITLE`=work title, and `UNIT_PAGE_RANGE_OR_LENGTH`=known length or empty. For chaptered works use `UNIT_DISPLAY_LABEL`=`Chapter <number>`, `UNIT_TITLE`=chapter title, and `UNIT_PAGE_RANGE_OR_LENGTH`=known page range/length. For standalone-stories-as-chapters route, keep the landing page to bibliographic metadata, coverage, advisory if relevant, and chapter/story navigation; remove the plot-summary and whole-work-analysis sections.

## `chapter.html` (one file per chapter, spoiler-safe)

| Placeholder | Content |
|---|---|
| `BOOK_TITLE`, `CHAPTER_NUMBER`, `CHAPTER_TITLE`, `EXPECTED_CHAPTER_COUNT`, `CHAPTER_PAGE_RANGE_OR_LENGTH` | Chapter identity and edition coverage |
| `CHAPTER_SUMMARY` | Concise summary of this chapter |
| `CHARACTERS_AND_INTERACTIONS`, `CHARACTER_DEVELOPMENT` | Who appears, how they interact, how they change |
| `EVENTS_AND_CONFLICTS` | Key events, conflicts, turning point; label unnamed events as coined |
| `EARLIER_CHAPTER_CONNECTIONS` | Links to earlier events in the same continuous narrative with chapter numbers; for standalone stories presented as chapters, omit unless the story itself establishes a relevant link |
| `SETTING_AND_CONTEXT` | Place, time, atmosphere |
| `CULTURAL_AND_REAL_WORLD_CONTEXT` | References and real-world events, with confidence noted and source links placed beside claims |
| `TONE_AND_MOOD`, `SYMBOLS_AND_MOTIFS`, `NARRATIVE_TECHNIQUES` | Craft observations |
| `ENDING_AND_OPEN_THREADS` | How the chapter ends and what remains unresolved |
| `CHAPTER_CONTENT_ADVISORY` | Optional concise, non-graphic warning for mature material in this chapter; omit when not relevant |
| `CHAPTER_EVIDENCE_AND_NOTES` | Chapter references, selective short quotes, and relevant external sources (publisher/site, title, URL; access date when available) |
| `GENRE_LENS_ANALYSIS` | Optional analysis using only applicable genre guides; omit if it adds no distinct insight |
| `CHAPTER_ADAPTATION_LENS` | Optional, separately labelled observations about this chapter's adaptation-relevant story function; omit the section if not useful |
| `WHOLE_WORK_ANALYSIS_LINK` | Whole-work analysis navigation anchor for routes that include such a page; replace with empty text for standalone-stories-as-chapters route |
| `PREVIOUS_CHAPTER_LINK`, `NEXT_CHAPTER_LINK` | `<a class="button-link button-secondary" href="chapter-NN.html">…</a>`; omit at the first or last chapter |

## `book-analysis.html` (spoilers allowed)

| Placeholder | Content |
|---|---|
| `BOOK_TITLE`, `LAST_CHAPTER_FILE` | Title and the final chapter's file name |
| `CHARACTER_ARCS`, `THEMES_AND_MESSAGE`, `PLOT_STRUCTURE_AND_CAUSALITY` | Whole-book synthesis |
| `FORESHADOWING_AND_PAYOFFS`, `SYMBOLISM_EVOLUTION` | Setups, payoffs, symbols over time |
| `NARRATIVE_CONSISTENCY`, `RELATIONSHIP_DYNAMICS` | Craft and relationships across the book |
| `RESOLUTION_AND_INTERPRETATIONS` | Ending, final message, alternative readings |
| `GENRE_LENS_ANALYSIS` | Optional whole-work genre synthesis from applicable genre guides; omit if it adds no distinct insight |
| `BOOK_ADAPTATION_LENS` | Optional, separately labelled adaptation-planning observations across the story; omit the section if not useful |
| `SOURCES_AND_NOTES` | External sources and caveats |

## `collection-index.html` (multiple independent works)

| Placeholder | Content |
|---|---|
| `VOLUME_TITLE`, `VOLUME_EDITOR_OR_COMPILER`, `VOLUME_EDITION` | Verified volume metadata |
| `VOLUME_COVERAGE` | Scope of contents actually available/analyzed |
| `COLLECTION_DESCRIPTION_AND_COVERAGE` | Brief volume description and coverage notes, without implying one unified plot |
| `VOLUME_SOURCES` | Sources supporting volume/contents metadata |
| `WORK_LIST_ITEMS` | One list item per identifiable work, in published order |

Per work list item: `WORK_INDEX_FILE`, `WORK_ORDER`, `WORK_TYPE`, `WORK_TITLE`, `WORK_AUTHOR_AND_COVERAGE`.

## `work-analysis.html` (single story or work without chapters)

| Placeholder | Content |
|---|---|
| `WORK_TITLE`, `VOLUME_TITLE`, `WORK_TYPE`, `WORK_AUTHOR_AND_COVERAGE` | Work identity and coverage |
| `WORK_SUMMARY_AND_STRUCTURE` | Spoiler-marked whole-work summary and structure |
| `WORK_CHARACTER_ARCS`, `WORK_PLOT_AND_CAUSALITY`, `WORK_THEMES_AND_CRAFT`, `WORK_RESOLUTION` | Whole-work story synthesis |
| `WORK_GENRE_ANALYSIS` | Optional applicable genre lens |
| `WORK_SOURCES_AND_NOTES` | Sources and uncertainty |

## Optional adaptation lens

The skill may add a clearly labelled adaptation-lens section to a chapter or whole-book page when useful. Keep it separate from the literary analysis and focus on story-planning observations: causal dramatic spine, major turns, character goals and stakes, visually significant settings or motifs, and moments that rely on internal thought or narration. Do not add screenplay scenes or dialogue unless requested. If adding a placeholder, add it to the matching HTML template and document it here.

## Citation and content safety

- Link an external source next to the claim it supports; include source/publisher, page title, and URL in source notes, plus access date when available.
- Prefer primary sources, publishers, libraries, and reputable reference works. Use sources only when they informed the claim; qualify uncertainty and avoid overstating what a source establishes.
- Escape plain-text replacement values for HTML. Only intentional, minimal structural markup should be inserted; never include scripts, event-handler attributes, or untrusted markup.
- An age/content advisory informs readers but does not override model content limits. Do not disguise or transform restricted content to evade those limits; explain a processing limitation and offer a permitted high-level alternative when possible.
