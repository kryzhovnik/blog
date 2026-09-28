# Роуты с поддоменами в Rails 4.2+

Недавно я обновлял старый rails 3.2 сайт на 4.2. Сайт обслуживает множество региональных поддоменов: один и тот же инстанс rails-приложения обслуживает region1.site.com и region99.site.com. Логика сайта предполагает, что со страниц одного поддомена могут быть ссылки на страницы другого. Поэтому на этом сайте уже давно применялся подход "_url-роуты по умолчанию вместо _path-роутов": важно не забывать, когда генерируешь ссылку, что она может вести на соседний поддомен.

Для указания поддомена на нашем сайте использовался старый хак из Railscasts [#221 Subdomains in Rails 3](http://railscasts.com/episodes/221-subdomains-in-rails-3):

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

Хак основан на том, что все роуты в rails 3 генерируются через этот метод [ActionView::Helpers::UrlHelper#url_for](https://github.com/rails/rails/blob/2553bd785c0b41193257851ac0267515ec3c9dc3/actionpack/lib/action_view/helpers/url_helper.rb#L100).
В четвертых рельсах похожую функцию (через него проходят цепочки генерации всех роутов) выполняет другой метод с таким же названием [ActionDispatch::Http::URL.url_for](https://github.com/rails/rails/blob/e7c68d0a4d5c84db107e43c9cc4f7baee2ed00b1/actionpack/lib/action_dispatch/http/url.rb#L31). И как оказалось, в новых рельсах эти хаки не нужны: роут-хелперы начиная с четвертой версии поддерживают опцию `subdomain: subdomain`.

Мне же все равно пришлось немного похачить, потому что у нас использовался другой вариант: где роль опции `subdomain`, выполняла опция `region`, принимающая объект откуда извлекался поддомен. Это позволило вместо `post_url(post, subdomain: region.subdomain)` писать `post_url(post, region: region)` - на 10 символов короче!

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

