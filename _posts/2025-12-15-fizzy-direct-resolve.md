---
layout: post
title: "Diving into Fizzy's Routes: Rails' resolve and direct"
date: 2025-12-15
description: "Exploring two underused Rails routing features — direct and resolve — through 37signals' newly open-sourced Fizzy codebase. Learn how to create custom URL helpers and teach Rails to generate polymorphic URLs for models without their own routes."
og_image:
  canvas:
    background_image: "/assets/images/og-backgrounds/bg-4190.png"
---

37signals [open-sourced](https://x.com/dhh/status/1995895084789772629) their latest product last week. I cloned it and started where I always start when exploring a new Rails app: config/routes.rb.

I think `config/routes.rb` is the best place to crack open any Rails codebase. It's the table of contents — you instantly see what resources exist, how they're nested, and the overall shape of the domain. In Fizzy's case: Accounts, Boards, Cards, Columns, Comments, Webhooks, Notifications.

But then I spotted something I'd honestly never used in production:

```ruby
# config/routes.rb
direct :published_board do |board, options|
  route_for :public_board, board.publication.key
end

direct :published_card do |card, options|
  route_for :public_board_card, card.board.publication.key, card
end

resolve "Comment" do |comment, options|
  options[:anchor] = ActionView::RecordIdentifier.dom_id(comment)
  route_for :card, comment.card, options
end

resolve "Mention" do |mention, options|
  polymorphic_url(mention.source, options)
end

resolve "Notification" do |notification, options|
  polymorphic_url(notification.notifiable_target, options)
end

resolve "Event" do |event, options|
  polymorphic_url(event.eventable, options)
end

resolve "Webhook" do |webhook, options|
  route_for :board_webhook, webhook.board, webhook, options
end
```

What are `direct` and `resolve`?

### Custom URL Helpers with `direct`

`direct` creates custom named URL helpers. Fizzy boards can be published publicly with a shareable link — but the public URL uses `publication.key` instead of the board's ID. Rather than building this URL manually every time, direct gives you published_board_url(board) and published_card_url(card).

```erb
<%# app/views/public/cards/show.html.erb %>
<%= tag.meta property: "og:url", content: published_card_url(@card) %>
```

You could achieve the same with a helper method. Here's the comparison:

**Using `direct` in routes.rb:**

```ruby
# config/routes.rb
direct :published_board do |board, options|
  route_for :public_board, board.publication.key, options
end
```

**Traditional helper in app/helpers/:**

```ruby
# app/helpers/boards_helper.rb (hypothetical alternative)
module BoardsHelper
  def published_board_path(board, options = {})
    public_board_path(board.publication.key, options)
  end

  def published_board_url(board, options = {})
    public_board_url(board.publication.key, options)
  end
end
```

The `direct` version defines both `_path` and `_url` automatically from a single block (though for public shareable links, you'd only ever need `_url`). Honestly, the helper version looks simpler and more straightforward. The advantage of `direct` is locality: all URL-generation logic lives in `routes.rb`.

Another bonus: `direct` helpers are automatically available in `Rails.application.routes.url_helpers`, so you can use them in models, background jobs, or anywhere outside controllers and views:

```ruby
Rails.application.routes.url_helpers.published_board_url(board)
```

One thing that confused me at first: `direct` and `resolve` routes don't appear in `rails routes` output. This is by design — they're URL *generation* helpers, not HTTP endpoints. A `direct` can even point to an external URL:

```ruby
# config/routes.rb
direct :homepage do
  "https://rubyonrails.org"  # Not a route in your app!
end
```

### Customizing Polymorphic URLs with `resolve`

The [Rails docs](https://api.rubyonrails.org/classes/ActionDispatch/Routing/Mapper/CustomUrls.html#method-i-resolve) dedicate about two sentences to `resolve`: "Define custom polymorphic mappings of models to URLs" and a brief example with a Basket model.

You know how `link_to @post` generates `/posts/123`? That's `polymorphic_url` under the hood — Rails introspects the model and finds the matching route.

But what happens when a model doesn't have its own route? Comments in Fizzy don't live at /comments/:id — they're displayed on their parent Card. Events are polymorphic wrappers around other actions. Notifications point to something else the user should see.

Without `resolve`, you'd write helpers like this everywhere:

```ruby
# app/helpers/comments_helper.rb
def comment_url(comment)
  card_url(comment.card, anchor: dom_id(comment))
end
```

And then remember to call `comment_url(comment)` instead of `url_for(comment)`. The `resolve` DSL fixes this — it teaches Rails how to generate URLs for specific model classes, keeping route logic in routes.rb where you'd naturally look for it.

The block receives:
1. The model instance
2. An options hash (anchors, format, etc.)

It returns whatever route_for or polymorphic_url can handle.

Both live in the same [CustomUrls module](https://api.rubyonrails.org/classes/ActionDispatch/Routing/Mapper/CustomUrls.html), both take a block that returns something `url_for` can handle.

<div class="collapsible">
<div class="collapsible-header">
  <p class="collapsible-title">Under the Hood: How resolve Actually Works</p>
  <p class="collapsible-subtitle">Step-by-step source code walkthrough</p>
</div>
<div class="collapsible-content" markdown="1">

The docs are sparse, so let's read the source. When you write:

```ruby
# config/routes.rb
resolve "Comment" do |comment, options|
  route_for :card, comment.card, options
end
```

Here's what Rails does at boot time.

**Step 1: The DSL method** ([mapper.rb](https://github.com/rails/rails/blob/main/actionpack/lib/action_dispatch/routing/mapper.rb#L2426))

```ruby
def resolve(*args, &block)
  unless @scope.root?
    raise RuntimeError, "The resolve method can't be used inside a routes scope block"
  end

  options = args.extract_options!
  args = args.flatten(1)

  args.each do |klass|
    @set.add_polymorphic_mapping(klass, options, &block)
  end
end
```

It validates you're at the root level (not inside a `namespace` or `scope`), then registers your block for each class name.

**Step 2: Store the mapping** ([route_set.rb](https://github.com/rails/rails/blob/main/actionpack/lib/action_dispatch/routing/route_set.rb#L674))

```ruby
def add_polymorphic_mapping(klass, options, &block)
  @polymorphic_mappings[klass] = CustomUrlHelper.new(klass, options, &block)
end
```

Your block gets wrapped in a `CustomUrlHelper` and stored in a hash:
`{ "Comment"=> [helper instance], ... }`.

**Step 3: The lookup** ([polymorphic_routes.rb](https://github.com/rails/rails/blob/main/actionpack/lib/action_dispatch/routing/polymorphic_routes.rb))

When you call `link_to(@comment)` or `url_for(@comment)`, Rails eventually hits `polymorphic_url`:

```ruby
def polymorphic_url(record_or_hash_or_array, options = {})
  if mapping = polymorphic_mapping(record_or_hash_or_array)
    return mapping.call(self, [record_or_hash_or_array, options], false)
  end
  # ... default polymorphic resolution
end

def polymorphic_mapping(record)
  _routes.polymorphic_mappings[record.to_model.model_name.name]
end
```

It checks the hash using the model's class name. If found, it calls your block instead of the default route resolution.

**Step 4: Execute the block** ([route_set.rb](https://github.com/rails/rails/blob/main/actionpack/lib/action_dispatch/routing/route_set.rb#L165))

```ruby
class CustomUrlHelper
  def call(t, args, only_path = false)
    options = args.extract_options!
    url = t.full_url_for(eval_block(t, args, options))
    only_path ? "/" + url.partition(%r{(?<!/)/(?!/)}).last : url
  end

  private
    def eval_block(t, args, options)
      t.instance_exec(*args, merge_defaults(options), &block)
    end
end
```

The helper runs your block via `instance_exec`, passing the model and options. Whatever you return gets passed to `full_url_for` to generate the final URL string.

**The complete flow:**

```
link_to(@comment)
  → url_for(@comment)
    → polymorphic_url(@comment)
      → polymorphic_mapping(@comment)
        → @polymorphic_mappings["Comment"]  # Your CustomUrlHelper
      → helper.call(self, [@comment, {}], false)
        → instance_exec(@comment, {}, &block)
          → route_for(:card, comment.card, anchor: "comment_123")
        → full_url_for([:card, card, {anchor: "comment_123"}])
          → "/cards/abc#comment_123"
```

Result: `link_to(@comment)` → `"/cards/abc#comment_123"`
</div>
</div>

### Fizzy's Patterns

**Notification → Whatever It's About**

```ruby
# config/routes.rb
resolve "Notification" do |notification, options|
  polymorphic_url(notification.notifiable_target, options)
end
```

Notifications wrap Events or Mentions. Rather than linking to a "notification show page" (boring), this links directly to the thing you're being notified about. The `notifiable_target` method is delegated to source:

```ruby
# notification.rb
delegate :notifiable_target, to: :source

# event.rb
def notifiable_target
  eventable  # Card, Comment, etc.
end

# mention.rb
def notifiable_target
  source  # The Card or Comment containing the @mention
end

# user.rb
def notifiable_target
  self  # "New user joined" → links to their profile
end
```

Now `link_to(@notification)` in the notification tray just works:

```ruby
# notifications_helper.rb
link_to(notification, class: "card card--notification", ...)
```

### Why This Matters

Fizzy has many "indirect" models — objects users interact with through their parents:

- Comments live on Cards
- Events describe actions on Cards/Comments
- Notifications wrap Events/Mentions
- Mentions point to Cards/Comments

The `direct` and `resolve` blocks centralize URL generation logic in routes.rb rather than burying it in helpers. You write `link_to(@notification)` and trust the router to figure it out. When someone asks "how do URLs work in this app?" — there's exactly one file to check.

It's one of those Rails features that's been there since Rails 5, hiding in plain sight. I've walked past it a hundred times in the docs. Seeing it used by the Rails creators themselves? Now I get it.

The [official docs](https://api.rubyonrails.org/classes/ActionDispatch/Routing/Mapper/CustomUrls.html#method-i-resolve) are sparse, but Fizzy's [config/routes.rb](https://github.com/basecamp/fizzy/blob/main/config/routes.rb) is a good example of real-world use cases.
