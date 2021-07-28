# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up

build:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --remove-orphans

test: up
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest api /tests/unit /tests/integration /tests/e2e

unit-tests:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest api /tests/unit

integration-tests: up
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest api /tests/integration

e2e-tests: up
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest api /tests/e2e

logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=25 api redis_pubsub

black:
	black -l 86 $$(find * -name '*.py')
