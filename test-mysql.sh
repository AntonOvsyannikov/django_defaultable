#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose-mysql.yml down
docker-compose -f docker-compose.yml -f docker-compose-mysql.yml up --build
docker-compose -f docker-compose.yml -f docker-compose-mysql.yml down

