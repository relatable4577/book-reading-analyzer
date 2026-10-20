# Compact JSON context

JSON is a handoff and retrieval format, not a token-saving format by itself. Use it to avoid repeatedly loading full prior chapters: store short, chapter-referenced facts and load only relevant records for the next analysis.

## Files

Keep context per narrative, not per physical volume. Treat context JSON as temporary working state by default. Store it in a unique run folder under the final output directory:

```text
<work-output>/
  .temp/
    <run-id>/
      source/
        <staged-book-copy>
      context/
        book-context.json
        chapters/
          chapter-001.json
```

For a collection, each work gets its own `book-context.json`; the volume has a separate `collection.json` catalog, all under the run's `context/` directory. Do not mix unrelated characters, themes, or events into shared context.

For EPUB input, keep the extraction `manifest.json` and source-section text in `.temp/<run-id>/epub-extracted/`. The manifest is provenance and boundary-review input, not a substitute for chapter analysis. Do not copy full extracted chapter text into JSON context records.

Before staging, create a unique run directory so existing temporary work is not overwritten. Copy the source book into its `source/` subdirectory and analyze the copy; never edit, move, or delete the original. By default, remove only this run's temporary directory after final output validation. If the user requested retention at the beginning, keep the run directory and report its path. Do not delete pre-existing `.temp` contents or another run's files. Keep the generated HTML and assets outside `.temp/` so they remain available after temporary cleanup.

## Book context responsibilities

`book-context.json` is a compact evolving index. Keep verified work/edition identity, genre classification with confidence, coverage and gaps, concise character states and relationships, significant event labels and causal links, themes/motifs/open threads, and external sources actually used. Keep every claim tied to evidence/unit references. Do not duplicate plot summaries or chapter prose. Preserve uncertainty; update affected entries when corrected text arrives.

## Per-chapter record responsibilities

`chapters/chapter-NNN.json` stores this unit's analysis concisely: summary, participants, character changes, events, prior-unit links, setting/context, genre-specific observations, narrative craft, ending/open threads, evidence locations, and sources. Store no full chapter text. Prefer page/paragraph locators to copying text.

## Context handoff

For each new unit, provide only:
1. current unit text and identifier;
2. work metadata and coverage status;
3. relevant character/event/theme/open-thread entries from `book-context.json`;
4. only the applicable genre lens or lenses;
5. any specific prior chapter record needed to resolve a callback.

After analysis, write the chapter record and update compact book context in the run's temporary `context/` directory. For synthesis, use these records and retrieve staged source text only to verify a specific detail. For HTML rendering, use structured records; do not reload the entire book into context.

If a chapter is too long for the available context, analyze bounded portions, retain locators, and synthesize one chapter record only after considering all portions. Avoid chapter-wide conclusions before that synthesis.

## Templates

- [Book context JSON](../templates/context/book-context.json)
- [Chapter context JSON](../templates/context/chapter-context.json)
- [Collection catalog JSON](../templates/context/collection.json)

These are valid JSON starter records. Replace values with verified data and preserve valid JSON; omit or leave empty irrelevant optional collections rather than storing full prose.
