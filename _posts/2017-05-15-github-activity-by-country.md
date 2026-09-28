---
layout: post
title: "GitHub Activity by Country"
date: 2017-05-15
written_around: 2017
published_in: 2026
description: "Commits per user by country, from the GHTorrent dataset in BigQuery and a small Ruby script."
tags: [github, bigquery, ruby, data]
---

A few years ago I listened to Professor Auzan's lectures on economics. In one of them he said that altruistic behavior used to be considered typical of people in developing countries, but that this is no longer the view. I thought then that I could try to check this claim with GitHub statistics: look at how active users from different countries are. Of course, activity on GitHub is not purely altruistic, but my intuition is that altruism makes a large part of it.

In [Google Cloud BigQuery](https://bigquery.cloud.google.com/) I found a public GitHub dataset, `ghtorrent-bq`. I ran two queries.

1) The number of users from each country:

```sql
SELECT COUNT(*) AS users_count, country_code AS country_code
  FROM [ghtorrent-bq:ght.users]
  WHERE country_code IS NOT NULL GROUP BY country_code
  ORDER BY users_count desc
```

2) The number of commits from each country:

```sql
SELECT COUNT(*) AS commit_count, users.country_code AS contry_code
  FROM [ghtorrent-bq:ght.commits] commits
  INNER JOIN [ghtorrent-bq:ght.users] users ON users.id = commits.author_id
  WHERE users.country_code is not null
  GROUP BY contry_code
  ORDER BY commit_count desc
```

I am not much of an SQL expert, so I calculated the ratios in a script. I calculated them only for the top 100 countries by number of users and commits. Without this limit, the top of the rating went to a country with the code "nu", North Korea, and the Central African Republic.

```ruby
require 'csv'
require 'iso_country_codes'
require 'markdown-tables'

def read_csv(filename)
  records = CSV.open(filename).to_a
  records = records[1..-1]

  records.map { |count, code| [code, count.to_i] }
    .sort_by(&:last).reverse
    .first(100).to_h
end

users = read_csv('/Users/kr/Downloads/users.csv')
commits = read_csv('/Users/kr/Downloads/commits.csv')

rating = (commits.keys & users.keys).map do |country_code|
  rate = 1.0 * commits[country_code] / users[country_code]
  country = IsoCountryCodes.find(country_code).name
  [country, country_code, rate.to_i]
end.sort_by(&:last).reverse

rating.map { |country, country_code, rate| [country, country_code, rate.to_i].join("\t") }
rating = rating.map.with_index(1).to_a.map {|a, i| a.unshift i}

labels = ['#', 'Country Name', 'Code', 'Rating']
data = rating

table = MarkdownTables.make_table(labels, data, is_rows: true, align: ['l', 'l', 'l', 'r'])

puts MarkdownTables.plain_text(table)
```

The result:

| # | Country | Code | Rating |
|--:|---|---|--:|
| 1 | Greece | gr | 619 |
| 2 | Switzerland | ch | 246 |
| 3 | Czechia | cz | 234 |
| 4 | Germany | de | 232 |
| 5 | Finland | fi | 212 |
| 6 | Luxembourg | lu | 205 |
| 7 | Austria | at | 200 |
| 8 | France | fr | 200 |
| 9 | Japan | jp | 196 |
| 10 | Uruguay | uy | 195 |
| 11 | Slovenia | si | 193 |
| 12 | Belgium | be | 192 |
| 13 | Canada | ca | 191 |
| 14 | Norway | no | 189 |
| 15 | United Kingdom of Great Britain and Northern Ireland | gb | 188 |
| 16 | United States of America | us | 187 |
| 17 | Estonia | ee | 186 |
| 18 | New Zealand | nz | 183 |
| 19 | Taiwan | tw | 182 |
| 20 | Netherlands | nl | 180 |
| 21 | Sweden | se | 174 |
| 22 | Israel | il | 172 |
| 23 | Australia | au | 165 |
| 24 | Denmark | dk | 164 |
| 25 | Italy | it | 158 |
| 26 | Poland | pl | 157 |
| 27 | Bulgaria | bg | 152 |
| 28 | Spain | es | 149 |
| 29 | Singapore | sg | 142 |
| 30 | Hungary | hu | 142 |
| 31 | Russian Federation | ru | 141 |
| 32 | Myanmar | mm | 139 |
| 33 | Slovakia | sk | 135 |
| 34 | Korea (Republic of) | kr | 135 |
| 35 | Argentina | ar | 132 |
| 36 | Lithuania | lt | 128 |
| 37 | Costa Rica | cr | 128 |
| 38 | Romania | ro | 128 |
| 39 | Croatia | hr | 126 |
| 40 | China | cn | 125 |
| 41 | Moldova (Republic of) | md | 124 |
| 42 | Ukraine | ua | 124 |
| 43 | Iceland | is | 123 |
| 44 | Georgia | ge | 122 |
| 45 | Ireland | ie | 122 |
| 46 | Portugal | pt | 116 |
| 47 | Sri Lanka | lk | 114 |
| 48 | Panama | pa | 111 |
| 49 | Belarus | by | 110 |
| 50 | Latvia | lv | 105 |
| 51 | Thailand | th | 103 |
| 52 | South Africa | za | 100 |
| 53 | Jamaica | jm | 100 |
| 54 | Cuba | cu | 98 |
| 55 | Kenya | ke | 97 |
| 56 | Brazil | br | 95 |
| 57 | Azerbaijan | az | 93 |
| 58 | Malaysia | my | 92 |
| 59 | Colombia | co | 90 |
| 60 | Jordan | jo | 90 |
| 61 | Cyprus | cy | 89 |
| 62 | Mexico | mx | 89 |
| 63 | Philippines | ph | 89 |
| 64 | Venezuela (Bolivarian Republic of) | ve | 87 |
| 65 | Ecuador | ec | 86 |
| 66 | El Salvador | sv | 83 |
| 67 | Serbia | rs | 83 |
| 68 | Viet Nam | vn | 83 |
| 69 | Chile | cl | 83 |
| 70 | Benin | bj | 82 |
| 71 | Peru | pe | 81 |
| 72 | Uganda | ug | 81 |
| 73 | Lebanon | lb | 79 |
| 74 | Armenia | am | 78 |
| 75 | Cambodia | kh | 78 |
| 76 | Guatemala | gt | 78 |
| 77 | Bosnia and Herzegovina | ba | 77 |
| 78 | Bolivia (Plurinational State of) | bo | 76 |
| 79 | Honduras | hn | 76 |
| 80 | Paraguay | py | 75 |
| 81 | United Arab Emirates | ae | 75 |
| 82 | Ghana | gh | 68 |
| 83 | Kazakhstan | kz | 68 |
| 84 | Turkey | tr | 65 |
| 85 | Nigeria | ng | 64 |
| 86 | Egypt | eg | 64 |
| 87 | Nepal | np | 63 |
| 88 | Indonesia | id | 63 |
| 89 | Iran (Islamic Republic of) | ir | 62 |
| 90 | Dominican Republic | do | 61 |
| 91 | India | in | 56 |
| 92 | Algeria | dz | 54 |
| 93 | Macedonia (the former Yugoslav Republic of) | mk | 52 |
| 94 | Bangladesh | bd | 48 |
| 95 | Morocco | ma | 48 |
| 96 | Saudi Arabia | sa | 43 |
| 97 | Tunisia | tn | 39 |
| 98 | Pakistan | pk | 38 |

Greece in first place, and with such a lead, also looks odd. Otherwise the claim seems to hold: the more prosperous the country, the more active its users.

Done. I am crossing the oldest item off my to-do list. Phew :)
