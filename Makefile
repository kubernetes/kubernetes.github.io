HUGO_VERSION      = $(shell grep ^HUGO_VERSION netlify.toml | tail -n 1 | cut -d '=' -f 2 | tr -d " \"\n")
NODE_BIN          = node_modules/.bin
NETLIFY_FUNC      = $(NODE_BIN)/netlify-lambda

# The CONTAINER_ENGINE variable is used for specifying the container engine. By default 'docker' is used
# but this can be overridden when calling make, e.g.
# CONTAINER_ENGINE=podman make container-image
CONTAINER_ENGINE ?= docker
IMAGE_REGISTRY ?= gcr.io/k8s-staging-sig-docs
IMAGE_VERSION=$(shell scripts/hash-files.sh Dockerfile Makefile | cut -c 1-12)
CONTAINER_IMAGE   = $(IMAGE_REGISTRY)/k8s-website-hugo:v$(HUGO_VERSION)-$(IMAGE_VERSION)
CONTAINER_RUN     = $(CONTAINER_ENGINE) run --rm --interactive --tty --volume $(CURDIR):/src

CCRED=\033[0;31m
CCEND=\033[0m

.PHONY: all build build-preview help serve

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

module-check:
	@git submodule status --recursive | awk '/^[+-]/ {err = 1; printf "\033[31mWARNING\033[0m Submodule not initialized: \033[34m%s\033[0m\n",$$2} END { if (err != 0) print "You need to run \033[32mmake module-init\033[0m to initialize missing modules first"; exit err }' 1>&2

module-init:
	@echo "Initializing submodules..." 1>&2
	@git submodule update --init --recursive --depth 1

all: build ## Build site with production settings and put deliverables in ./public

build: module-check ## Build site with production settings and put deliverables in ./public
	hugo --minify

build-preview: module-check ## Build site with drafts and future posts enabled
	hugo --buildDrafts --buildFuture

deploy-preview: ## Deploy preview site via netlify
	hugo --enableGitInfo --buildFuture -b $(DEPLOY_PRIME_URL)

functions-build:
	$(NETLIFY_FUNC) build functions-src

check-headers-file:
	scripts/check-headers-file.sh

production-build: build check-headers-file ## Build the production site and ensure that noindex headers aren't added

non-production-build: ## Build the non-production site, which adds noindex headers to prevent indexing
	hugo --enableGitInfo

serve: module-check ## Boot the development server.
	hugo server --buildFuture

docker-image:
	@echo -e "$(CCRED)**** The use of docker-image is deprecated. Use container-image instead. ****$(CCEND)"
	$(MAKE) container-image

docker-build:
	@echo -e "$(CCRED)**** The use of docker-build is deprecated. Use container-build instead. ****$(CCEND)"
	$(MAKE) container-build

docker-serve:
	@echo -e "$(CCRED)**** The use of docker-serve is deprecated. Use container-serve instead. ****$(CCEND)"
	$(MAKE) container-serve

container-image: ## Build a container image for the preview of the website
	$(CONTAINER_ENGINE) build . \
		--network=host \
		--tag $(CONTAINER_IMAGE) \
		--build-arg HUGO_VERSION=$(HUGO_VERSION)

container-build: module-check
	$(CONTAINER_RUN) --read-only --mount type=tmpfs,destination=/tmp,tmpfs-mode=01777 $(CONTAINER_IMAGE) sh -c "npm ci && hugo --minify"

container-serve: module-check ## Boot the development server using container. Run `make container-image` before this.
	$(CONTAINER_RUN) --cap-drop=ALL --cap-add=AUDIT_WRITE --read-only --mount type=tmpfs,destination=/tmp,tmpfs-mode=01777 -p 1313:1313 $(CONTAINER_IMAGE) hugo server --buildFuture --bind 0.0.0.0 --destination /tmp/hugo --cleanDestinationDir

test-examples:
	scripts/test_examples.sh install
	scripts/test_examples.sh run

.PHONY: link-checker-setup
link-checker-image-pull:
	$(CONTAINER_ENGINE) pull wjdp/htmltest

docker-internal-linkcheck:
	@echo -e "$(CCRED)**** The use of docker-internal-linkcheck is deprecated. Use container-internal-linkcheck instead. ****$(CCEND)"
	$(MAKE) container-internal-linkcheck

container-internal-linkcheck: link-checker-image-pull
	$(CONTAINER_RUN) $(CONTAINER_IMAGE) hugo --config config.toml,linkcheck-config.toml --buildFuture
	$(CONTAINER_ENGINE) run --mount type=bind,source=$(CURDIR),target=/test --rm wjdp/htmltest htmltest

clean-api-reference: ## Clean all directories in API reference directory, preserve _index.md
	rm -rf content/en/docs/reference/kubernetes-api/*/

api-reference: clean-api-reference ## Build the API reference pages. go needed
	cd api-ref-generator/gen-resourcesdocs && \
		go run cmd/main.go kwebsite --config-dir ../../api-ref-assets/config/ --file ../../api-ref-assets/api/swagger.json --output-dir ../../content/en/docs/reference/kubernetes-api --templates ../../api-ref-assets/templates
