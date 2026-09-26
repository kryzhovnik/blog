# Blog design and copy review

Last updated: 2026-09-26

## Working agreement

- Discuss one review item at a time: proposal, discussion, implementation.
- Keep this file current so the review survives session compaction.
- Do not edit article bodies. Frontmatter descriptions, templates, styles, and About copy may change after discussion.
- Replies to the user are in Russian. Site copy and repository files are in English.
- This `docs` directory is excluded from the Jekyll output in `_config.yml`.

## Accepted changes

- The homepage has no personal introduction. Keep the blog name `Commit Messages`.
- The site title is neutral, 1.5rem, weight 700. A blue `✳` precedes it on the homepage; a thin blue `←` takes the same space on other pages. Both are part of the home link. Only the words are underlined on hover.
- Navigation uses `About me`, except on About where it uses `Posts` linking home. Do not use `Andrey` as the navigation label.
- Links use the blue accent, including post titles on the homepage. The blog title is the color exception.
- On the homepage, dates appear above post titles. Post titles use weight 600. The header gap above the list is 2.5rem.
- The theme follows the OS setting. The switcher was removed; the user rejected putting it in the footer.
- About has the author's name, `Software maker`, location, portrait, and the approved short copy in `about.md`. The unpublished language-learning app is mentioned without naming it. The DropKind name links to its public site.
- The About portrait appears on the left at desktop and mobile sizes, at 180px and 96px respectively. The About page has a shorter mobile gap below the header.
- The homepage descriptions for Fizzy, Generative UI, and word pronunciation were shortened. The other four descriptions were retained. Keep Jev in the Chat Modes description; readers know it.
- Mobile article body text is 18px; block code retains the previous size.
- The footer has the year and author on the left and RSS on the right. There is no RSS link after each article.
- Articles have a minimal navigation row before comments with `← All posts`. A related link appears only where the topic warrants it. `_data/related_posts.yml` contains three links: Chat Modes ↔ Generative UI, and word pronunciation → Chat Modes. The other four posts have no related link.

## Rejected or excluded

- Do not restore any homepage introduction or tagline. The user rejected `Making software. Figuring things out.` after seeing it on the site.
- Do not narrow the desktop reading width to 700px. The user tried it and asked to restore the original width.
- Do not turn related links into cards or add a separate explanation block. The user wants the minimal navigation row.
- Do not use journal-like About copy describing what the author writes about.
- Do not use the sentence `My work spans customer-facing features and the back-office tools that keep those businesses running.`
- Do not edit article bodies.

## Next item

Social preview images were raised but the user deferred discussion. Some cards show a hashtag row when a post has tags, while others do not. The candidate is to remove the visible hashtag row while keeping tag metadata. No change has been approved or implemented.

All accepted site changes above are implemented. The existing untracked `assets/images/og/posts/ruby-llm-modes.png` predates this review and is outside the review commit.
