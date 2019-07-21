#!/bin/bash

rm -f db.sqlite3
docker-compose up --build
docker-compose down

