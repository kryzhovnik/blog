---
layout: post
title: "Dictionary-Quality Word Pronunciation Without Dictionary APIs"
date: 2025-12-19
description: "How to build reliable word pronunciation for language learning apps using LLM-based TTS instead of dictionary APIs. Covers handling heteronyms with IPA substitution and building a practical pronunciation pipeline."
---

When I started building word pronunciation features for my language learning app, the obvious first idea was to pull audio files from "reputable" dictionaries — Oxford, Cambridge, Collins, etc.

But I quickly ran into limitations:

- **Access.** Getting an API key can be a hassle even for testing.
- **Rate limits.** Restrictions on requests and pricing.
- **Caching.** Storing audio locally is often prohibited — which is a dealbreaker for a learning app.
- **Vendor lock-in.** Once you commit to a specific dictionary (its article structure, response formats, definition markup, pronunciation quirks), adding other languages becomes painful. Each language has its own dictionaries and formats, and stitching them together cleanly gets messy fast.

So I ended up with a solution I'd been avoiding: LLM-based Text-to-Speech. I'd tried similar things a year or so ago — back then, the quality wasn't good enough for "dictionary-grade" pronunciation. But there's been noticeable progress in both the models and available APIs since then: with the right setup, the results are now quite practical.

### System Instructions: A Separate Channel for Style Control

APIs let you pass system instructions separately from the text. This is useful because you can treat them as a "contract" for pronunciation style:

- accent variant: British / American;
- delivery: clear, neutral, steady pace — closer to a dictionary narrator than a voice actor.

That's enough to get consistent "educational" audio instead of "theatrical line readings."

### Heteronyms: The Model Will Be Wrong "Sometimes," but You Need "Never"

Then came a less obvious problem — heteronyms: words spelled the same but pronounced differently depending on context (part of speech, meaning, tense).

The classic example is *read*:

- present: /riːd/
- past: /rɛd/

You can try to tweak the system instructions so the model always picks the right variant from context — but reliability will still be hit or miss. And in a learning app, mispronunciation is a bad experience: the user will memorize the wrong pattern.

### IPA Substitution: Explicit Phonetics Instead of Guessing

The most practical trick turned out to be simple: replace the ambiguous word with IPA (International Phonetic Alphabet).

Example:

- We read (present) → We /riːd/
- We read (past) → We /rɛd/

You turn ambiguous spelling into unambiguous phonetics, and TTS no longer "guesses" — it just pronounces exactly what you've specified.

### IPA on Demand

You don't want to generate IPA for all text all the time: it's more expensive and more complex. So here's the approach:

1. Check the text: does it contain any words from a small list of heteronyms (a candidate dictionary)?
2. If not — send it straight to TTS.
3. If yes — make an additional request to an LLM tuned for the short task "pick the correct pronunciation":
   - word + sentence/context;
   - (optionally) structural hints from your context, e.g.: `{pos: "verb", tense: "past"}`;
   - output: IPA or a choice between variants.
4. Replace the word in the text with `/ipa/`.
5. Send the "phonetic-ready" text to TTS.

The key idea: the extra request only fires when there's a real risk of mispronunciation.

### The Final Pipeline

**Before:**
```
text → TTS LLM → audio
```

**After:**
```
text + context + user-prefs → heteronyms → IPA → system instructions → cache → TTS LLM → audio
```

More steps, but they give you full control over exactly what makes dictionary APIs seem "more reliable": style, pronunciation, and caching.

### On Quality

The best part: quality turned out better than I expected.

I tested the results on Russian — not exactly a top-tier target language for TTS products. There's an accent, but it's barely noticeable: far less than any non-native speaker, and even less than many bilinguals. For second-language learning, that's more than good enough.
