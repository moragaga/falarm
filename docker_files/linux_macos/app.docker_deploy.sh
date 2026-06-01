#!/bin/bash
docker compose -f ./docker_files/docker-compose.app.local.yml down
docker compose -f ./docker_files/docker-compose.app.local.yml build --no-cache
docker network inspect cosmosdb-local-runtime-network >/dev/null 2>&1 \
  || docker network create cosmosdb-local-runtime-network
docker compose -f ./docker_files/docker-compose.app.local.yml up -d