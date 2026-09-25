---
layout: post
title: "Typography test page"
date: 2000-01-01
description: "Every element kramdown can emit. Visible only with `make drafts`."
sitemap: false
---

Paragraph with **bold**, *italic*, `inline code`, a [link](/), <kbd>Cmd</kbd>+<kbd>K</kbd>, <mark>marked text</mark>, ~~deleted~~ <del>text</del>, H<sub>2</sub>O, x<sup>2</sup>, an <abbr title="HyperText Markup Language">HTML</abbr> abbreviation, and a footnote.[^1]

Second paragraph, long enough to wrap onto a few lines so that the line height and the spacing between paragraphs are easy to judge. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

## Lists

- Item one
- Item two
  - Nested item
  - Nested item
    1. Deep ordered
    2. Deep ordered
- Item three

1. First
2. Second

   A second paragraph inside the list item.

3. Third

Definition term
: Definition text.

Another term
: Another definition.

## Table

| | Gemini 3.5 Flash Lite | Jev |
|---|---:|---:|
| routing time, median | 765 ms | 351 ms |
| cost per 1000 turns | $0.29 | $0.04 |
| a long cell that should wrap or scroll on narrow screens | 1 234 567 | 7 654 321 |

| Left | Center | Right |
|:---|:---:|---:|
| a | b | c |

## Quote

> A quote with **bold** text.
>
> Second paragraph of the quote.

## Code

```ruby
class ChatMode
  def call(message) = classifier.pick(message)
end
```

<details markdown="1">
<summary>Native details element</summary>

Hidden content.

</details>

---

Text after a horizontal rule.

[^1]: Footnote text with a [link](/).
