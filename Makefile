# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up
reload: down up

build:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d database-es database-it application rabbitmq redis mailhog mongo mongo-express

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --remove-orphans

test: up
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/unit /var/www/tests/integration /var/www/tests/e2e

unit-tests:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest application /tests/unit

integration-tests: up
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest application /tests/integration

e2e-tests: up
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --no-deps --entrypoint=pytest application /tests/e2e

logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=25 application

run-workers:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d worker

reload-workers:
	docker-compose restart worker
