# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

SITE=
ENV=development

SERVICE=

all: down build up
reload: down up

network:
	docker network create nlp_net

build:
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml build

up:
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml up -d database application rabbitmq redis mailhog mongo mongo-express

down:
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml down --remove-orphans

test: up
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.development.yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/unit /var/www/tests/integration /var/www/tests/e2e

unit-tests:
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.test.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/unit

integration-tests: up
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.development.yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/docker-compose.development.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/integration

e2e-tests: up
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.development.yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/docker-compose.development.yml run --rm --no-deps --entrypoint=pytest application /var/www/tests/e2e

logs:
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml -f ./docker/compose/$(SITE)/docker-compose.yml -f ./docker/compose/$(SITE)/docker-compose.$(ENV).yml logs --tail=25 application

run-workers:
	docker-compose -p nlp.$(SITE) -f ./docker/compose/docker-compose.yml -f ./docker/compose/docker-compose.$(ENV).yml up -d worker

reload-workers:
	docker-compose -p nlp.$(SITE) restart worker
