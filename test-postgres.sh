#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose-postgres.yml down
docker-compose -f docker-compose.yml -f docker-compose-postgres.yml up --build
docker-compose -f docker-compose.yml -f docker-compose-postgres.yml down

