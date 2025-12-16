# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
make install    # Install dependencies (bundle install)
make start      # Start dev server (bundle exec jekyll serve)
make build      # Build site (bundle exec jekyll build)
make clean      # Remove _site and .jekyll-cache
```

## Architecture

This is a minimal Jekyll 4.4 blog with custom layouts and SCSS styling.

**Key directories:**
- `_posts/` - Blog posts (YYYY-MM-DD-title.md format)
- `_layouts/` - HTML templates (default.html wraps everything, post.html extends default)
- `assets/css/` - SCSS stylesheets processed by Jekyll

**Configuration:**
- `_config.yml` - Site settings, permalink structure (/:title/), kramdown markdown with rouge syntax highlighting
- `Gemfile` - Dependencies: jekyll, jekyll-feed, jekyll-seo-tag

**Layout hierarchy:** post.html -> default.html

## Writing Posts

Create files in `_posts/` with front matter:
```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
---
```
