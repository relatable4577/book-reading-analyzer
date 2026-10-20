# Collections, anthologies, and omnibus volumes

First establish whether the supplied volume contains one continuous narrative or multiple distinct works. Check its contents page and reliable metadata; use the actual supplied text to determine boundaries. Never infer that every heading is a separate work or that every included work is complete.

## Classify the volume

- **One narrative with internal parts/books:** Treat as one work when the causal plot and narrative continuity remain one story. Preserve the author's parts as structure; do not create separate work folders just because the novel has multiple "books".
- **Standalone stories presented as chapters:** Treat each identifiable story as a separate chapter-level analysis unit, even if the contents page calls them chapters or the volume gives them chapter numbers. Create one analysis page per story/chapter, but no additional whole-book or story-cycle analysis page and no volume-wide synthesis. Separate units may reuse character names, settings, or motifs without establishing one continuous narrative.
- **Linked story cycle:** Analyze each story on its own first. Connect recurring characters or events across stories only when the text supports that identity and continuity; shared names alone are insufficient. A clearly labeled collection-level note may discuss substantiated links, but do not force independent plots into one continuous arc.
- **Omnibus or Reader's Digest-style volume of separate novels:** Create a collection landing page and a separate story map for each included novel. Each novel map has its own home, chapter pages, and whole-book analysis, limited to the supplied (possibly condensed/abridged) text. A sequel in a series gets its own novel analysis; do not merge it with the preceding novel. The collection landing page is a catalog only, not a volume-wide plot summary or synthesis.
- **Anthology/short-story collection:** If each story is presented as a chapter/unit, follow the standalone-stories route: one chapter page per story and no additional work-level or volume-wide analysis page. If the stories have no chapter divisions, create one work-level page per story. In either case, keep independent stories separate.
- **Abridged or edited collection (including Reader's Digest selections):** State that the supplied work is abridged/edited when verified. Analyze only the provided version, identify missing or unknown coverage, and do not claim to analyze the complete unabridged work.
- **Unclear or mixed volume:** List identifiable contents and boundaries. Keep unknown contents explicitly unknown; if needed, limit analysis to known works rather than inventing a catalog.

## Output layout

For route (2), use a collection root and one child directory per included novel. For route (3), use a navigation-only landing page and chapter pages at the volume level, with one page per standalone story/chapter and no whole-volume analysis. If a story itself has meaningful chapters within a multiple-novel volume, its novel child directory contains the normal chapter pages:

Route (2) folder example:

```text
<repository-root>/<volume-slug>/
  index.html                  # volume metadata, coverage, contents, links only
  assets/
  works/
    01-<work-slug>/
      index.html              # that work's overview
      book-analysis.html      # that work's synthesis, if enough text is available
      chapter-001.html
      assets/
    02-<work-slug>/
      ...
  .temp/                       # temporary processing data, not final deliverables
    <run-id>/
      source/                  # staged copy of supplied volume
      epub-extracted/          # EPUB extraction output, if applicable
      context/
        collection.json
        <work-slug>/
          book-context.json
          chapters/
            chapter-001.json
```

Use [collection-index.html](../templates/collection-index.html) for the volume landing page. Keep `collection.json` and each work's context records in the run's temporary `.temp/<run-id>/context/` directory, not among the final HTML deliverables. Each work folder follows the normal story-map workflow; do not share character/event context across unrelated works. For a story without chapters, use [work-analysis.html](../templates/work-analysis.html) rather than inventing chapter pages.

## Analysis scope

- The collection landing page identifies the volume, describes coverage/edition at a high level, and lists works in the published order with separate links. It is not a narrative synthesis.
- Do **not** produce one whole-volume plot, character arc, or conclusion that merges unrelated works. For route (2), each constituent novel gets its own whole-book analysis where the supplied coverage supports one. For route (3), do not create additional story-level analyses; the individual chapter/story pages are the complete requested analysis.
- For standalone stories presented as chapters, produce only the chapter/story pages and a navigation-only landing page. Do not generate a separate analysis page for each story or a combined book analysis; do not combine their context records. Shared names alone do not establish identity.
- For multi-novel Reader's Digest-style volumes, each novel gets its own chapter pages and whole-book analysis based on the available text. The volume-level page lists the novels and coverage only; it does not provide a combined plot, character arc, or conclusion.
- For an omnibus of connected novels, do not combine novels into one book analysis. A cross-volume series synthesis is optional and should be added only if requested, clearly separated from each novel's analysis.
- A collection-level note about editorial order, framing, or recurring themes is optional only when the user requests it. Label it as collection-level editorial analysis, not as a unified story analysis. For standalone-stories-as-chapters route, do not add collection-level analysis by default.
- A work that itself contains chapters gets chapter pages. A standalone short story without chapter divisions gets a single work-level analysis page instead of fabricated chapter pages.

## Progress and safeguards

- Record work identity, order, author, form (novel/story/excerpt), and coverage status in `collection.json`.
- Verify metadata for the containing volume and each included work when useful. Cite sources and note uncertainty/edition differences.
- Track chapter progress and continuity inside that work's own context file. Never carry spoilers from a later chapter into an earlier chapter page.
- If only some works or excerpts were supplied, mark each work's status (not started, partial, analyzed, or unavailable) and avoid conclusions about missing text.
- For route (2), the collection home is a catalog of included novels and their coverage, with no volume-wide plot summary; detailed endings and payoffs stay on each novel's analysis page with a spoiler warning. For route (3), the landing page is navigation and bibliographic metadata only.
