---
layout: post
title: "Sequence Is Not Structure"
date: 2026-07-28
description: "Long LLM conversations preserve sequence, not structure. I want a way to see where ideas branch, drift, and remain unfinished."
tags: [llm, ux, thinking-tools]
---

One of the prompts I use most often now is: “Explain this to me as if I were a smart ten-year-old.” The models have become good enough to outrun me. They can generate a dense argument in seconds; I may need an hour to understand it and fit it into everything else we have discussed. The bottleneck is no longer the model but me.

<figure>
  <img src="/assets/images/posts/sequence-is-not-structure/01-me-and-my-smart-friends.jpeg" alt="The 'me vs my smart friends' meme: a neanderthal labelled ME next to two men in suits labelled MY SMART FRIENDS">
</figure>

I usually open a session full of enthusiasm, with a question that has been circling at the edge of my mind and has finally taken shape in words. The LLM points out what I have missed, each question produces five more, and the field of inquiry expands without anything pulling it back toward an answer. The dopamine hits; I feel very smart. Three hours later, I have ten interesting directions, no answers, and only a vague memory of where I started.

A lot of my longer sessions begin to feel like *Lost*: every answer opens another interesting mystery until there are more threads than any ending could possibly resolve. Plenty of intrigue, no meaningful conclusion.

Chat is often an excellent interface, but it exposes little of the conversation's structure. This becomes especially limiting in long exploratory conversations, where the question itself evolves and the dialogue becomes part of the thinking process.

## Text became cheap. Understanding did not.

For most of human history, every additional line of text consumed material, time, and labor. The medium imposed a kind of conservation law: ideas were compressed partly by the cost of reproducing them.

LLMs removed most of the cost of producing another page. Chat often feels like `llm | human`, except the human side is lossy: most of the output gets dropped before I can integrate it.

<figure>
  <img src="/assets/images/posts/sequence-is-not-structure/04-llm-processing-expectation-vs-reality.jpg" alt="Two conveyor belts: one running neatly and another overflowing with food and boxes, captioned as how an LLM thinks its answers are processed versus how they are actually processed">
</figure>

When the stream becomes unmanageable, I ask the model to turn it into another text: a summary, a plan, a specification, a handoff. These artifacts are useful, often necessary. But compression is lossy: it makes the conversation manageable by discarding some of the detail and connections that made it valuable in the first place.

What I want is not simply less text, but another way to hold its structure. We gave text infinite room to expand, but gave thought no coordinates.

## Thinking in space

I keep returning to a familiar scene: people thinking together around a whiteboard or a table covered with notes. They talk, but they also draw, connect, rearrange, and point. The conversation occupies space.

<figure>
  <img src="/assets/images/posts/sequence-is-not-structure/02-platos-academy-mosaic.jpg" alt="Roman mosaic from Pompeii showing a group of philosophers gathered around an object on the ground, one of them pointing at it with a stick">
  <figcaption>Plato's Academy, mosaic from Pompeii, 1st century BC. The stick is what holds the attention in one place.</figcaption>
</figure>

A teacher can draw an empty circle, spend five minutes explaining it, and then return to the whole argument by pointing at the circle again. The students do not need the explanation repeated. The circle has acquired a location and a history. It has become a place inside the conversation.

<figure>
  <img src="/assets/images/posts/sequence-is-not-structure/03-feynman-blackboard.jpg" alt="Richard Feynman lecturing in front of a blackboard covered with equations, diagrams and boxed results">
  <figcaption>The blackboard keeps the whole argument in view at once.</figcaption>
</figure>

## Sequence is not structure

Chat has no equivalent of that circle. Every idea enters the same vertical stream and becomes another message. Forty messages later, an important thought is still there, but nothing in the current view points back to it. I have to remember that it exists before I can search for it.

A transcript preserves sequence, but sequence is not structure. A line of thought can branch, stall, merge with another, or remain unfinished. Chat flattens all of this into before and after. It shows only the order of messages and the distance between them.

This is what makes drift so difficult to notice. Every reply can be useful on its own and follow naturally from the one before it. There may be no single wrong turn. Yet after a few hours, I can find myself deep inside a secondary detail, with several important questions left unresolved behind me. The conversation moved through twenty reasonable steps, but I can no longer explain where it is going.

> **Change is not drift**
>
> An exploratory conversation should be allowed to change direction. A new branch may be a discovery, a useful pivot, or the natural evolution of the original idea. It becomes drift when the transition goes unnoticed — when we can no longer explain how we got here or what we left unresolved behind us.

## A missing dimension

I wonder whether long exploratory conversations could grow a visual structure alongside the text. It would evolve with the conversation, making ideas and their relationships visible instead of compressing them into another document afterward.

What I miss in those sessions is orientation: I want to see the conversation as a whole, understand the relationships between its parts, and know where the current line of inquiry sits inside it. The transcript tells me what came before. It does not show me where I am.

Notes help once a thought has settled. During exploration, they can be stale four messages later because the question itself has changed. Branching leaves me with two transcripts to get lost in instead of one.

Maybe the answer is simply a canvas beside the chat. I have not used one enough to know whether maintaining it by hand provides orientation or becomes another system to manage.

I also have no idea what an automatically growing layer should look like. A graph can turn into spaghetti even faster than a chat turns into a wall of text. This post is mostly a structured dump of accumulated frustration — which I have, appropriately, expressed by producing yet another long text artifact.

If you have found a way to stay oriented in long conversations with LLMs — not merely summarize them afterward, but keep track of their shape while they unfold — I would really like to hear about it.
