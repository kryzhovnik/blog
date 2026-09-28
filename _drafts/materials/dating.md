# Dating the posts from old notes

Source: `~/code/technotes/blog.md`. The file has no git history, and its mtime (2022-05-03) comes from a copy, so the dates below come from the text itself. The notes in the file appear in this order: CSRF, subdomain routes, …, GitHub activity. This order is likely chronological.

## Where Does Rails Keep CSRF Tokens? — around 2015 (date: 2015-08-15)

- The note describes Rails 4.2 as the current version ("starting with Rails 4.2") and links to `4-2-stable`. Rails 4.2 came out in December 2014; Rails 5.0 came out in June 2016.
- Token masking (rails/rails#16570) was merged in August 2014 and shipped in 4.2.
- The linked lines L266–L271 on `4-2-stable` still point at `masked_authenticity_token`. The file on that branch last changed in February 2015.
- No mention of Rails 5 features (per-form CSRF tokens).
- It comes before the subdomain note in the file.
- The exact day is a guess inside that window.

## Subdomain Routes in Rails 4.2+ — around 2015 (date: 2015-09-01)

- "Recently I upgraded an old Rails 3.2 site to 4.2."
- The link to `ActionDispatch::Http::URL.url_for` uses commit `e7c68d0a` on master. That is a merge commit from 2015-09-01 04:33 UTC. The next commits on master came several hours later, so this was the HEAD of master when the permalink was copied. This dates the note to about 2015-09-01.

## GitHub Activity by Country — around 2017 (date: 2017-05-15)

- The script uses `MarkdownTables.plain_text`. The `markdown-tables` gem first came out on 2017-04-16; `plain_text` was added on 2017-04-17.
- `iso_country_codes` returns "Czechia". The gem renamed "Czech Republic" to "Czechia" on 2017-03-09.
- The table has "Macedonia (the former Yugoslav Republic of)". The country became North Macedonia in February 2019.
- The dataset `ghtorrent-bq` and the classic BigQuery UI (`bigquery.cloud.google.com`) fit this period.
- Window: April 2017 – early 2019. The note is the last one in the file, and it says "crossing the oldest item off my to-do list". Spring 2017 is the most likely time.
