# Analysis kickoff and workflow

Use this short decision process before analyzing content. It guides the analysis; do not reveal private chain-of-thought. Share concise conclusions, uncertainty, and requested outputs only.

## Intake checklist

1. **Confirm the source.** Identify whether the book is attached, pasted, or available at a user-provided path. If none is available, ask the user for the file path or to attach/paste it before analyzing. Do not guess a location or search unrelated directories. If a path cannot be accessed in the current environment, say so and request an accessible upload or text.
2. **Classify the material.** Decide whether the input is a single narrative, a series installment, a novel with internal parts, an anthology of independent stories, an omnibus of multiple novels, an abridged collection, or a partial excerpt. Do not assume that a volume equals one narrative, or that chapter headings define narrative units.
3. **Identify the available evidence.** Record what text is actually supplied, its chapter/work boundaries, any title/author/edition/translation clues, and the user's goal. Keep supplied text as the authority for literary analysis.
4. **Check context and constraints.** Verify relevant contents/edition metadata before analysis; identify coverage gaps, model/content limitations, and spoiler boundaries.
5. **Select analysis lenses.** Identify likely primary and secondary genres, then load only the matching [genre lenses](./genre-lenses/README.md). Genres may overlap; avoid forcing a single label or applying every lens.
6. **Choose exactly one output route.** (1) A continuous novel gets a book home, chapter pages, and one whole-book analysis. (2) A volume containing multiple novels gets a collection catalog and, for each novel, its own home, chapter pages, and book analysis; do not create a volume-wide plot summary or synthesis. (3) A volume whose chapters are standalone stories gets a navigation-only landing page and chapter/story pages only; do not create a combined book/story-cycle analysis.
7. **Stage safely.** By default, use `<repository-root>/<book-slug>/` for the final output and create a unique `<repository-root>/<book-slug>/.temp/<run-id>/` working directory. Keep generated book folders outside `.github/skills/story-map/`. Copy the source book there without modifying or moving the original; store any pasted text, extraction output, and context records under this run directory.
8. **Maintain evidence-based state.** Keep textual observations, external facts, and interpretations distinct. Update compact JSON context after each analyzed unit in `.temp/<run-id>/context/` and refer back to stored notes rather than repeating all earlier text.
9. **If the input is EPUB, extract and review.** Use the optional [local EPUB workflow](../scripts/README.md): deterministic local parsing of the staged copy's package metadata, TOC, spine, and text first; then model review of candidate boundaries and inclusion/exclusion labels. Inspect actual boundary text when metadata/excerpts leave ambiguity. Never call a spine item a chapter without validating it.
10. **Clean up safely.** After validating final HTML, delete only this run's temporary directory by default. Retain it only if the user requested retention at the start. Never remove pre-existing or other-run files.

## Analysis unit

- For a novel with chapters, analyze each chapter in sequence.
- For a short story or other work without meaningful chapter divisions, analyze it as a whole; do not invent chapters. Use the work-level analysis page.
- For a volume containing multiple novels (including condensed or abridged Reader's Digest-style volumes), treat each novel as its own analysis unit with its own chapter pages and whole-book analysis, using only the supplied version. The volume landing page is a catalog, not a volume-wide story summary.
- If each chapter is a self-contained or disconnected story, keep one chapter page per story and stop at chapter-level analysis. Do not create an extra work-analysis/book-analysis page or a combined volume-wide synthesis. A shared name alone does not establish that two appearances are the same character or that the stories form one continuous plot.
- Carry character identity, events, and continuity across story boundaries only when the text provides evidence, such as explicit identification or clear causal/narrative links. If the connection is uncertain, keep the stories' analyses and context separate, state the uncertainty, and do not build a combined character arc or ending from it.
- If boundaries or contents are uncertain, explain the uncertainty and analyze only identifiable material.

## Genre-aware practice

Use the shared baseline from `SKILL.md` for every narrative. Add only the appropriate genre-specific questions from the genre references. For mixed genres, combine applicable lenses without duplicating the baseline. A genre lens is an interpretive aid, not a checklist that must produce an observation for every chapter.

Genre guides:
- [Mystery and thriller](./genre-lenses/mystery-thriller.md)
- [Fantasy and science fiction](./genre-lenses/speculative-fiction.md)
- [Romance](./genre-lenses/romance.md)
- [Horror](./genre-lenses/horror.md)
- [Historical fiction](./genre-lenses/historical-fiction.md)
- [Literary fiction](./genre-lenses/literary-fiction.md)
- [Nonfiction and memoir](./genre-lenses/nonfiction-memoir.md)
- [Adventure and quest narratives](./genre-lenses/adventure-quest.md)
- [Comedy and satire](./genre-lenses/comedy-satire.md)
- [Coming-of-age and young adult](./genre-lenses/coming-of-age.md)
- [Family saga and social drama](./genre-lenses/family-saga-drama.md)
- [War and political fiction](./genre-lenses/war-political.md)

## Continuity and token efficiency

- Store a concise `book-context.json` per narrative/work and one `chapter-NNN.json` per analyzed chapter; use the structures in [context-json.md](./context-json.md).
- Persist compact facts, state changes, event links, open questions, and evidence locations—not chapter prose or a duplicate of the full analysis.
- For a new chapter, provide the chapter text plus only relevant metadata and the compact context needed to understand callbacks. Retrieve an older chapter record only when a specific callback requires it.
- JSON is structured storage, not inherently a token-saving format. Reduce repeated input by keeping records concise and selectively loading relevant entries.
- Build or revise the HTML from saved chapter records and synthesis after analysis. Do not reload the entire book merely to render pages.
- If one chapter is too long for the available context, analyze bounded portions, label their evidence locations, then synthesize the portions into one chapter record. Do not make whole-chapter claims until all portions have been considered.
