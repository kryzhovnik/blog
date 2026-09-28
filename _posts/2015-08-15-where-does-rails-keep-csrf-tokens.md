---
layout: post
title: "Where Does Rails Keep CSRF Tokens?"
date: 2015-08-15
written_around: 2015
published_in: 2026
description: "CSRF tokens live in the session; since Rails 4.2 the token on the page changes on every load, but it is only the session token masked with XOR."
tags: [rails, security, csrf]
---

TL;DR: Rails keeps CSRF tokens in the session: `session[:_csrf_token]`. In Rails >= 4.2 the token on the client changes on every page load, but it is only the session token masked with XOR.

## What is Cross-Site Request Forgery (CSRF)

It is an attack like this:

1. You are logged in to good-site.com (you are always logged in to many good sites).
2. You open a page on evil-site.com.
3. Without you noticing, the page on evil-site.com builds and sends a request to good-site.com to delete your account: `https://good-site.com/account/destroy`.
4. Because you are logged in to good-site.com, the request is authenticated and runs. Your account is gone!

## How do you protect against it?

To make this attack impossible, sites use CSRF tokens. A token is a long string, unique for each session on the site. The client (the code in the browser) adds this token to every non-GET request, that is, to every request that can change the state of the system. Before the server runs the request, it compares the received token with the token in the current session.

## How does Rails implement this protection?

_In broad strokes:_

1. It generates a unique token for each session:

```ruby
session[:_csrf_token] ||= SecureRandom.base64(AUTHENTICITY_TOKEN_LENGTH)
```

2. It puts a hidden field with this token into forms:

2.1. For forms built with `form_for` or `form_tag`, it adds the hidden field right when it renders the form on the server:

```html
<input type="hidden" name="authenticity_token" value="DB9fbHNOeLZSFc7XJEG0DERO0uOOcxdKF+uc4BDrwFVFJgRkdFUt/rNKVP0QgUz8wRftrYsUG/T9kd6ivbju/g==">
```

2.2. For Ajax requests, and for forms built on the fly in the browser, you put the `<%= csrf_meta_tag %>` helper into the page `<head>`. It generates meta tags with the token value:

```html
<meta name="csrf-param" content="authenticity_token">
<meta name="csrf-token" content="DB9fbHNOeLZSFc7XJEG0DERO0uOOcxdKF+uc4BDrwFVFJgRkdFUt/rNKVP0QgUz8wRftrYsUG/T9kd6ivbju/g==">
```

JavaScript can read the value from there. `jquery_ujs`, for example, does exactly that.

## Q&A

Q: So where are these tokens stored?

— In the session!

```ruby
session[:_csrf_token] ||= SecureRandom.base64(AUTHENTICITY_TOKEN_LENGTH)
```

Q: What is the point? By default Rails stores the session in a cookie, so the client can read it.

— It can't. Rails encrypts the session on the server, so only the server can read its data.

Q: Then why, starting with Rails 4.2, does the token string in the browser change on every page load?

— That is true: the browser gets a new token on every page load. But each new token is only a representation of the single real token stored in the session. The changing token does not make CSRF protection any stronger. It is there to mitigate a completely [different attack](http://breachattack.com/). The new token is built so that it does not look like the original, but the original can still be recovered from it.

```ruby
# https://github.com/rails/rails/blob/4-2-stable/actionpack/lib/action_controller/metal/request_forgery_protection.rb#L266-L271
def masked_authenticity_token(session)
  one_time_pad = SecureRandom.random_bytes(AUTHENTICITY_TOKEN_LENGTH)
  encrypted_csrf_token = xor_byte_strings(one_time_pad, real_csrf_token(session))
  masked_token = one_time_pad + encrypted_csrf_token
  Base64.strict_encode64(masked_token)
end
```

In plain terms, masking:

```
masked_token = random + (random XOR real_token)
```

Unmasking:

```
random = first half of masked_token
real_token = (second half of masked_token) XOR random
```
