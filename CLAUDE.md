# CLAUDE.md

Personal Jekyll blog "Commit Messages" at https://msg.samsonov.io. Plain CSS (no SCSS), custom layouts, no theme gem. Commands live in the `Makefile`; `make drafts` serves the site with `_drafts/` included.

Pushing `main` deploys: GitHub Actions builds the site and publishes it to GitHub Pages (`.github/workflows/jekyll.yml`). Push only when the user asks.

## Post lifecycle

1. **Draft.** Run `bin/draft "<Title>"` (or `/draft`). It creates `_drafts/<slug>.md` and `_drafts/materials/<slug>/`. Materials hold sources, notes, and diagram inputs; the build excludes them. Commit as `Draft: <Title>`.
2. **Images.** Put published images in `assets/images/posts/<topic>/` with an ordered prefix (`00-…`, `01-…`). Draw diagrams with the `diagram` skill.
3. **Publish.** `git mv` the draft to `_posts/YYYY-MM-DD-<slug>.md`, set `date`, then run `make build` to generate the OG card at `assets/images/og/posts/<slug>.png`. Commit the post and the PNG together as `Publish: <Title>`.

Front matter:

```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
description: "One sentence."   # homepage list, SEO, llms.txt, and the .md alternate
tags: [ruby, rails]            # also rendered as a hashtag row on the OG card
og_image:                      # optional; `make og-background` prints this block
  canvas:
    background_image: "/assets/images/og-backgrounds/bg-XXXX.png"
---
```

Permalinks are `/:year-:month-:day-:title/`, so the file name fixes the URL. Treat a published file name as permanent.

## OG images

`jekyll-og-image` writes PNGs into the source tree with `force: false`, so it skips any PNG that already exists.

- Commit every generated PNG. On a clean checkout the first build generates the PNG but does not copy it into `_site`, so CI would ship the post without its card.
- After a change to a post's title, tags, or background, delete its PNG and rebuild; otherwise the card stays stale.
- Keep `force: false`. With `force: true`, the running dev server copied a truncated PNG into `_site` while the plugin was rewriting it.

## Other moving parts

- `_plugins/markdown_alternate.rb` serves each post's raw Markdown at `/<slug>.md`; `llms.txt` lists these URLs for LLM agents.
- `_data/related_posts.yml` maps a post URL to one related post, shown above comments. Add an entry only when the topics really connect.
- Comments are Giscus (GitHub Discussions), configured in `_layouts/post.html`.
- The stylesheet URL carries `site.github.build_revision` for cache busting.
- `_private/` is git-ignored and excluded from the build.
