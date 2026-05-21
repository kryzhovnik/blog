require "jekyll"

# For each post at /:slug/, generate a sibling page at /:slug.md that returns
# the post's raw Markdown source (with a short H1 + date header).
#
# Implementation note: the page is created with a .txt source extension so
# Jekyll's Markdown converter doesn't run on it, but the permalink ends in .md
# so the file is written to /:slug.md in the built site.
module Jekyll
  class MarkdownAlternateGenerator < Generator
    safe true
    priority :low

    def generate(site)
      site.posts.docs.each do |post|
        slug = post.url.gsub("/", "")
        next if slug.empty?

        page = PageWithoutAFile.new(site, site.source, "/", "#{slug}.txt")
        page.data["permalink"] = "/#{slug}.md"
        page.data["layout"] = nil
        page.data["sitemap"] = false
        page.content = build_content(post)

        site.pages << page
      end
    end

    private

    def build_content(post)
      lines = []
      lines << "# #{post.data['title']}"
      lines << ""
      lines << "*Published on #{post.date.strftime('%B %d, %Y')}*"
      lines << ""
      lines << "> #{post.data['description']}" if post.data["description"]
      lines << ""
      lines << "---"
      lines << ""
      lines.join("\n") + post.content
    end
  end
end
