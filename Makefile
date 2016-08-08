
default: build/index.html

build/index.html: slides.md
	mkdir -p build
	landslide -lno -i -d $@ $<
