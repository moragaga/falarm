#!/bin/bash
docker compose -f ./docker_files/docker-compose.cosmos.local.yml down
docker compose -f ./docker_files/docker-compose.cosmos.local.yml build --no-cache
docker compose -f ./docker_files/docker-compose.cosmos.local.yml up -d