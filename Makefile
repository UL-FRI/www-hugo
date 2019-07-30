.PHONY: default
default: hugo-dev-server

.PHONY: hugo-dev-server
hugo-dev-server:
	hugo server --ignoreCache --disableFastRender

.PHONY: hugo-build-prod
hugo-build-prod:
	hugo --minify -b $(url)

.PHONY: build-prod
build-prod: hugo-build-prod


.PHONY: hugo-build-dev
hugo-build-dev:
	hugo

.PHONY: build-dev
build-dev: hugo-build-dev


.PHONY: clean
clean:
	rm -rd public/
	rm -rd resources/