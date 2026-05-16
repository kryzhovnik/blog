# Generative UI Article v2 Design

## Goal
Create a bolder second draft of `_drafts/generative-ui-ruby-llm.md` in a new file, preserving the article's exploratory arc while making the final structured-output approach clearer, more accurate to the current gem, and leaner.

## Editorial shape
Keep the progression:

1. text chat baseline;
2. widget-via-tool as the first useful approximation;
3. the scaling/composition problem with one tool per top-level component;
4. UI as a flat tree rather than a graph;
5. `render_ui` as a useful but mismatched intermediate transport;
6. structured output as the natural transport for assistant replies;
7. `ruby_llm-generative_ui` as the library form of the final design.

The new draft should spend less time on discarded approaches and more time on the ideas that survive into the final architecture.

## Required corrections
- Replace “graph” framing with “flat tree”.
- In the handwritten `render_ui` stage, state explicitly that the prompt is still duplicated by hand and that this is a smell the gem later removes.
- Soften claims about transport behavior: structured output makes the desired shape natural and removes the extra post-tool turn; it does not mathematically prevent all duplication.
- Describe the one-tool-per-component problem precisely: composition is possible only by minting more special top-level tools, which causes scenario/tool proliferation.
- Align the gem section with the current implementation:
  - `ResponseSchema` is a shared permissive envelope schema, not generated from component classes.
  - component classes feed prompt instructions, validation allow-lists, and render-target resolution.
  - `MessageExtensions` reads stored structured content and validates the tree; it does not validate against `ResponseSchema`.
  - the repo link points to the gem author's repository, not the RubyLLM maintainer's.
- Mention two missing boundaries:
  - interactive components only render UI; turning a click into the next user turn remains application logic;
  - the app keeps the trust boundary through allow-listed components, server-side validation, and ordinary authorization for real actions.

## Compression strategy
- Shorten the `halt` detour.
- Replace the long partial example with only the essential rendering seam.
- Reduce the `render_ui` section to one representative example plus the architectural point.
- Avoid re-explaining envelope/catalog separation in both the structured-output and gem sections.
- Keep the gem section focused on what the library packages, not on duplicating README-level detail.

## Output
Create a new draft file alongside the original, tentatively `_drafts/generative-ui-ruby-llm-v2.md`, leaving the current draft untouched.
