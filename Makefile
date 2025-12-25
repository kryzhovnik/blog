.PHONY: start build install clean og-background

start:
	bundle exec jekyll serve

build:
	bundle exec jekyll build

install:
	bundle install

clean:
	rm -rf _site .jekyll-cache

og-background:
	@mkdir -p assets/images/og-backgrounds
	@SUFFIX=$$(openssl rand -hex 2); \
	SEED=$$RANDOM; \
	warpgrad -W 1200 -H 600 \
		--colors 'b9d7da;a5c8ca;f6eddc' \
		-w 15 -s 300 -t simplex -p random -n 25 \
		--seed $$SEED -f png \
		-o assets/images/og-backgrounds/bg-$$SUFFIX.png 2>/dev/null; \
	echo "Add to post front matter:"; \
	echo ""; \
	echo "og_image:"; \
	echo "  canvas:"; \
	echo "    background_image: \"/assets/images/og-backgrounds/bg-$$SUFFIX.png\""
