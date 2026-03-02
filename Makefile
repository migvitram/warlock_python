include .env

up:
	@docker compose -f ${DOCKER_CONFIG} up --force-recreate -d

up-log: # create and start containers
	@docker compose -f ${DOCKER_CONFIG} up

up-rebuild-log:
	@docker compose -f ${DOCKER_CONFIG} up --build --no-cache

down: # stop and destroy containers
	@docker compose -f ${DOCKER_CONFIG} down

down-v: #  WARNING: stop and destroy containers with volumes
	@docker compose -f ${DOCKER_CONFIG} down --volumes

start: # start already created containers
	@docker compose -f ${DOCKER_CONFIG} start

stop: # stop containers, but not destroy
	@docker compose -f ${DOCKER_CONFIG} stop

ps: # show started containers and their status
	@docker compose -f ${DOCKER_CONFIG} ps

build: # build all dockerfile, if not built yet
	@docker compose -f ${DOCKER_CONFIG} build --no-cache

shell:
	@docker compose -f ${DOCKER_CONFIG} exec -it python /bin/bash

images:
	@docker compose images

params ?= 
	
pytests:
	@docker compose -f ${DOCKER_CONFIG} exec python-tests bash -c "cd ./tests && pytest $(params)"