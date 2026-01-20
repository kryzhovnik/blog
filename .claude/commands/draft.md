---
model: haiku
---

# /draft Command Specification

Create a new blog post draft with associated materials directory.

## Usage

```
/draft <post-title>
/draft                  # prompts for title if not provided
```

## Arguments

- `$ARGUMENTS` - The post title (required, will prompt if missing)
  - Accepts human-readable titles: `"My Great Post"` → `my-great-post`
  - Accepts direct slugs: `my-great-post` → `my-great-post`
  - Auto-detects: if input contains spaces or uppercase, slugify; otherwise use as-is

## Slugification Rules

- Convert to lowercase
- Replace spaces with hyphens
- Transliterate accented characters (é → e, ñ → n)
- Convert `&` to `and`
- Remove all other special characters and punctuation
- Collapse multiple hyphens into one
- No maximum length limit

**Examples:**
- `"Café & Code: A Story!"` → `cafe-and-code-a-story`
- `"My First Post"` → `my-first-post`
- `"already-slugified"` → `already-slugified`

## Created Files

Given slug `<post-name>`:

### 1. Draft markdown file
**Path:** `_drafts/<post-name>.md`

**Contents:**
```yaml
---
layout: post
title: "<Original Title>"
date: <today's date YYYY-MM-DD>
description:
tags: []
---

```

### 2. Materials directory
**Path:** `_drafts/materials/<post-name>/`

Empty directory (no placeholder files).

## Behavior

### Conflict handling
If either `_drafts/<post-name>.md` OR `_drafts/materials/<post-name>/` already exists:
- **Fail with error**
- Do not create any files
- Print clear message indicating which path already exists

### Missing argument
If no argument provided or empty string:
- **Prompt for title** using AskUserQuestion or similar

### Output
On success, print only the created paths:
```
_drafts/<post-name>.md
_drafts/materials/<post-name>/
```

## Out of Scope

- Opening files in editor after creation
- Publishing drafts (moving to `_posts/`)
- Creating subdirectory structure in materials
- Template file support

## Implementation

Run the bash script: `bin/draft "<title>"`

The script handles all logic: slugification, conflict detection, directory creation, and file generation.
