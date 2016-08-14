
default: build/index.html

build/index.html: slides.md
	mkdir -p build
	landslide -lno -i -d $@ $<

push:
	scp build/index.html anandology.com:/var/www/anandology.com/presentations/generators-inside-out/
