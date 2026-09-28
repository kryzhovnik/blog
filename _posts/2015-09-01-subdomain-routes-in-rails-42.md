---
layout: post
title: "Subdomain Routes in Rails 4.2+"
date: 2015-09-01
written_around: 2015
published_in: 2026
description: "Upgrading a multi-subdomain site from Rails 3.2 to 4.2: the old url_for hack goes away, and a small patch keeps the region: option."
tags: [rails, routing, upgrade]
---

Recently I upgraded an old Rails 3.2 site to 4.2. The site serves many regional subdomains: one instance of the Rails app serves both region1.site.com and region99.site.com. By design, a page on one subdomain can link to pages on another. So this site had long used a "`_url` routes by default instead of `_path` routes" rule: when you generate a link, you must remember that it can lead to a neighboring subdomain.

To set the subdomain, the site used an old hack from Railscasts [#221 Subdomains in Rails 3](http://railscasts.com/episodes/221-subdomains-in-rails-3):

```ruby
# Include in view helpers
module UrlHelper
  def with_subdomain(subdomain)
    subdomain = (subdomain || "")
    subdomain += "." unless subdomain.empty?
    [subdomain, request.domain, request.port_string].join
  end

  def url_for(options = nil)
    if options.kind_of?(Hash) && options.has_key?(:subdomain)
      options[:host] = with_subdomain(options.delete(:subdomain))
    end
    super
  end
end

# Use in a view
<%= post_url(post, subdomain: region.subdomain) #=> http://region1.site.com/posts/1 %>
```

The hack works because in Rails 3 all routes are generated through this method: [ActionView::Helpers::UrlHelper#url_for](https://github.com/rails/rails/blob/2553bd785c0b41193257851ac0267515ec3c9dc3/actionpack/lib/action_view/helpers/url_helper.rb#L100).
In Rails 4 a different method with the same name does a similar job (the generation of every route goes through it): [ActionDispatch::Http::URL.url_for](https://github.com/rails/rails/blob/e7c68d0a4d5c84db107e43c9cc4f7baee2ed00b1/actionpack/lib/action_dispatch/http/url.rb#L31). And it turned out that the new Rails does not need these hacks at all: starting with version 4, route helpers support the `subdomain: subdomain` option.

I still had to hack a little, because we used a different variant: a `region` option did the job of the `subdomain` option. It took an object and got the subdomain from it. So instead of `post_url(post, subdomain: region.subdomain)` we could write `post_url(post, region: region)` — 13 characters shorter!

```ruby
# lib/region_as_subdomain_url_patch.rb

require 'action_dispatch/http/url'

module ActionDispatch::Http::URL
  class << self
    alias_method :original_full_url_for, :full_url_for

    def full_url_for(options)
      if options[:params].is_a?(Hash)
        if region = options[:params].delete(:region)
          options[:subdomain] = region.subdomain
        end
      end

      original_full_url_for(options)
    end
  end
end
```
