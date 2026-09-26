---
layout: post
title: "Chat Modes: Configuring the LLM for Each Turn"
date: 2026-09-25
description: "A real job for Jev: routing every chat turn to a mode with its own instructions, tools, model, and thinking."
tags: [rails, ruby-llm, llm, jev, chat-modes]
---

In my language-learning app, a learner can start a chat with either of these messages:

<figure>
  <img src="/assets/images/posts/chat-modes/00-two-turns.png" alt="Two chats. In the first, the learner sent the single word &quot;adjudicate&quot;. In the second, the learner sent &quot;make cards from Friends S2E3&quot;. In both, the assistant shows the same &quot;Reasoning…&quot; indicator.">
</figure>

The first is a bare word: the learner wants it explained, right now. The second is a job: find the show, check the episode is in the catalog, run the extraction, report back. Everything about a good reply differs between them:

| | "adjudicate" | "make cards from Friends S2E3" |
|---|---|---|
| what the user expects | explain the word, right now | find the show, check the episode is in the catalog, run the extraction, report back |
| tools | not needed | needed |
| thinking | not needed | needed |
| acceptable latency | every second before the first word feels like a slow dictionary | a few extra seconds are fine |
| cost of the turn | should be minimal | can be higher |

Each kind of request needs its own settings, and for the first kind, light settings are enough. But both can arrive in the same chat, to the same assistant. How do you give each turn the settings it needs?

Here is what I did: before each turn, a cheap classifier picks a mode, that is, the instructions, tools, model, and thinking for this one reply. The conversation history is shared; everything else changes from turn to turn. The question "who answers this turn" becomes a separate step in the application, one you can see in the log and test. It sounds like an extra call on every turn, but in my chat the replies got faster and more accurate, and the routing itself takes about 350 ms with Jev and costs four cents per thousand turns.

<figure>
  <img src="/assets/images/posts/chat-modes/01-one-configuration-vs-modes.svg" alt="Three turns of one conversation. With one configuration, every request carries the prompt of every mode and every tool. With modes, a request carries only the prompt and tools of the selected mode, and the history is shared.">
  <figcaption>What a request carries on each turn: one configuration vs. modes</figcaption>
</figure>

## The cost of one-size-fits-all

The simplest option for mixed requests is one configuration for the whole conversation: a shared system prompt, a shared set of tools, and one good model for every kind of turn. Skills in this setup are all attached up front too, and the model decides which one the turn needs. It is simple, but you pay for that simplicity on every turn.

- Tools and skills attached up front travel in every request, although a given turn needs only some of them. Latency and cost grow with the context.
- The more similar tools the model sees, the more often it picks the wrong one, and a wrong pick costs another round trip.
- One configuration means one thinking effort for every case. Explaining a word quickly needs no reasoning, while a five-step tool workflow needs it.
- The decision about which tool or skill to use is made by the answering model inside its own turn. It is not a separate boundary in the application that you can test independently of the reply.

Most LLM libraries let you change the model, tools, and thinking before every turn. The question is how to organize that so the configuration logic does not end up scattered across conditionals in the request handler.

## Chat modes

I use the term *chat mode*, or just *mode*, for a named configuration of one turn: instructions, tools, model, and thinking effort, described together under one name. A separate router chooses between modes. This is not several agents handing a task to each other; it is one chat whose configuration is chosen anew before every reply.

Two things are fixed:

- the part of the system prompt shared by all modes, which may be empty;
- the visible message history.

Everything else is decided on each turn:

message and history → classifier → mode → configured chat → reply

A small classifier looks at the last message and the history and decides what the user wants right now: explain a word, work with flashcards, deal with a TV show, or ask a clarifying question. The next message goes through the classifier again, and the mode may change.

The key property of this scheme is that the boundary between behaviors is made explicit: there is a finite set of named configurations — modes — and a separate, observable router decision. The model that answers the user never sees the tools and instructions of other modes, because the choice was made before it. Routing and each mode are tested independently.

Each mode also has a short description, and it works the same way as a tool description. The model reads tool descriptions to decide which tool to call; the router reads mode descriptions to decide which mode to pick.

One of the modes can be for clarifying questions. It handles messages that are ambiguous on their own: "delete it" with no card on screen, where guessing means risking the wrong action. In my app this mode is called `clarify`. It is not the same as fallback. Fallback kicks in when the classifier could not choose; the clarifying mode is something the classifier chooses confidently, because asking a question is the right response here. To the router it is an ordinary mode: its own description, a short prompt, low thinking effort, and no tools.

## The classifier

Intuition says the classifier should slow everything down: it is one more model call before every reply.

In my chat, the opposite happened, even before Jev, with a plain chat model, Gemini 3.5 Flash-Lite. Picking a mode takes under a second. In return, the answering model gets a short prompt, only the tools it needs, and a matching thinking effort. Replies got faster, and the model picked the wrong tool less often.

Jev is a new kind of model: it does not generate text. You give it a question with answer options, and it returns a probability for each option. Routing has exactly that shape: here are the mode descriptions, here are the last messages, who should answer. That makes routing one judge call instead of a structured-output chat call.

Numbers from my chat: the same turns through both classifiers. The Jev measurement was taken from Europe with the server in North America, so the time includes network overhead.

| | Gemini 3.5 Flash-Lite | Jev |
|---|---:|---:|
| routing time, median | 765 ms | 351 ms |
| cost of 1000 routing turns | $0.29 | $0.04 |

After switching from Flash-Lite to Jev, the decisions on my data matched almost 100% of the time.

Both classifiers also report how sure they are, but this confidence means different things. For Flash-Lite it is the model's self-assessment. Jev returns a full probability distribution over the modes, and confidence shows how concentrated it is on one option. So a confidence threshold must be tuned for each classifier separately.

## When the router is not sure

The classifier can be unsure, and it can fail. For both cases the router has a fallback mode and a confidence threshold. The router also returns the data behind each decision: what the classifier returned, its probabilities and confidence, whether fallback fired, and how long it took. I write this into the message meta. Here is the record for "exit the card", sent with a card open:

```json
{
  "mode_name": "tutor",
  "decided_by": "fallback",
  "reason": "Below confidence threshold",
  "decision": {
    "mode_name": "manage_cards",
    "confidence": 0.4,
    "reason": null,
    "probabilities": {
      "tutor": 0.27,
      "clarify": 0.18,
      "manage_cards": 0.55,
      "showtime": 0.0
    }
  },
  "duration_ms": 351,
  "classifier": {
    "with": "judge",
    "model": "jev-1.13.0"
  }
}
```

Here `manage_cards` got the highest probability, but the distribution was not concentrated enough: confidence 0.4 against a threshold of 0.5, so the router took the fallback `tutor`. On the same turn, Flash-Lite reported 0.95 for `manage_cards`, and the router would have gone straight there. When the intent is known without a classifier, for example the user clicked a button in the UI, the code can set the mode directly, and the record shows that too: `decided_by: caller`.

## Limitations

Modes help when different kinds of turns need different settings. If almost every turn in your chat ends up in the same heavy workflow anyway, there is nothing to separate, and routing only adds a step. The router also picks one mode for the whole turn: if one message mixes tasks from different modes, it will not split them. For that you need a broader mode or a separate decomposition step.

Modes are close to tool search: both narrow what the answering model sees. Tool search does it for tools only, and it helps when one kind of work has dozens of tools. A mode also changes the prompt, the model, and thinking effort, so it helps when the kinds of work themselves differ. The two can be used together.

The cost I noticed is prefix caching. With one configuration, every request starts with the same instructions and tools, and the provider's prefix cache hits well. Mode instructions go before the history, so when the mode changes, the prefix changes too, and that turn misses the cache. While the mode stays the same, the cache works as usual. In my chat, routing gives more than this takes away.

## RubyLLM::Modes

Everything above works in any stack. In Ruby, I packaged it as a [gem](https://github.com/kryzhovnik/ruby_llm-modes) on top of [RubyLLM](https://rubyllm.com).

### Modes

RubyLLM already provides `RubyLLM::Agent`, a class that declaratively defines a turn's configuration (instructions, tools, model, and thinking) and applies it to an existing chat. It is a ready-made base for a mode.

A mode adds one more field to that configuration: `description`, the same macro that `RubyLLM::Tool` has. RubyLLM::Modes adds `RubyLLM::ModeAgent`, a subclass of `Agent` with this field, and a router that reads it.

```ruby
class TutorAgent < RubyLLM::ModeAgent
  description "Explains words and grammar, corrects the learner, keeps the conversation going. A bare word or phrase is a request to explain it."

  instructions "You are a patient language tutor."
  thinking effort: :low
end

class ManageCardsAgent < RubyLLM::ModeAgent
  description "Creates, edits, or deletes flashcards. Only when the learner asks for it, never inferred from a word alone."

  instructions "Manage the learner's flashcards with the tools."
  tools CreateCard, UpdateCard, DeleteCard
  thinking effort: :medium
end
```

If your app already has its own agent base class, extend it with `RubyLLM::Modes::Mode` instead:

```ruby
class ApplicationAgent < RubyLLM::Agent
  extend RubyLLM::Modes::Mode
end
```

### The router

The router lists the modes, gives the classifier its own instructions (here: that a flashcard is open on screen), declares a fallback mode, and chooses which classifier to use:

```ruby
class ChatModeRouter < RubyLLM::Modes::Router
  inputs :user, :card

  mode TutorAgent
  mode ClarifyAgent
  mode ManageCardsAgent
  mode ShowtimeAgent

  instructions do
    "The learner has a flashcard open on screen." if card
  end

  history last: 6
  fallback TutorAgent, below_confidence: 0.5
  classify_with :judge
end
```

Applying it on each turn takes two lines: the router picks the mode, the mode configures the chat and runs the turn:

```ruby
route = ChatModeRouter.new(user:, card:).call(message.content, history: chat.messages)
route.mode(chat:).complete
```

`classify_with :judge` uses Jev through RubyLLM's judge API. Judge is already in RubyLLM's main; it is not in 2.0.0 yet. Switching the router to it is a one-line change.

### Try it

Code and examples are on [GitHub](https://github.com/kryzhovnik/ruby_llm-modes), the package is on [RubyGems](https://rubygems.org/gems/ruby_llm-modes).

I came to this approach out of real need, while I tuned and optimized my chats on the previous generation of models. It worked even then, but with Jev it feels complete: routing is now fast and cheap enough to run on every turn without a second thought. That is why I turned it into a gem and published it.

If your chat also mixes quick questions with heavy tasks, give modes a try. Start with two of them, and look at what the router log tells you. I would be glad to hear how it goes.
