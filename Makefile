SITE=
ENV?=development

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

.PHONY: help
help: ## Show make targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf " \033[36m%-20s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)

all: destroy build start ## Destroy, build and start container (destroy build start)
reload: stop start ## Reload container (stop start)

.PHONY: build
build: ## Build docker container
	@docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml build

start: CMD=up -d application ## Start container
stop: CMD=stop ## Stop container
destroy: CMD=down --remove-orphans ## Destroy container

start stop destroy:
	@docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml $(CMD)

.PHONY: test
test: unit-tests ## Run all tests

unit-tests: ## Run unit tests
	@docker-compose -p nlp.test -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.test.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/unit

e2e-tests: start ## Run end to end tests
	@docker-compose -p nlp.test -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.test.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/e2e

integration-tests: start ## Run integration tests
	@docker-compose -p nlp.test -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.development.yml -f ./docker/compose/test/docker-compose.yml -f ./docker/compose/docker-compose.development.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/integration

static-analysis: ## Run python linter
	@docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.test.yml run --rm --no-deps static-analysis


reload-workers: stop-workers run-workers ## Reload RabbitMQ workers

run-workers: CMD=up -d ## Run RabbitMQ workers
stop-workers: CMD=stop ## Stop RabbitMQ workers

stop-workers run-workers:
	@docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml $(CMD) worker
