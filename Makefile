export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

.PHONY: help
help: ## Show make targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf " \033[36m%-20s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)

all: destroy build start ## Destroy, build and start container (destroy build start)
reload: stop start ## Reload container (stop start)

.PHONY: build
build: ## Build docker container
	@docker-compose -f ./docker/docker-compose.yml build

start: CMD=up -d --force-recreate application ## Start container
stop: CMD=stop ## Stop container
destroy: CMD=down --remove-orphans ## Destroy container

start stop destroy:
	@docker-compose -f ./docker/docker-compose.yml $(CMD)

.PHONY: test
test: unit-tests ## Run all tests

unit-tests: ## Run unit tests
	@docker-compose -f ./docker/docker-compose.yml run --rm --no-deps --entrypoint="pytest /opt/code/tests/unit" application

e2e-tests: start ## Run end to end tests
	@docker-compose -f ./docker/docker-compose.yml run --rm --no-deps --entrypoint="pytest /opt/code/tests/e2e" application

integration-tests: start ## Run integration tests
	@docker-compose -f ./docker/docker-compose.yml run --rm --no-deps --entrypoint="pytest /opt/code/tests/integration" application

reload-workers: stop-workers run-workers ## Reload RabbitMQ workers

run-workers: CMD=up -d ## Run RabbitMQ workers
stop-workers: CMD=stop ## Stop RabbitMQ workers

stop-workers run-workers:
	@docker-compose -f ./docker/docker-compose.yml $(CMD) worker
