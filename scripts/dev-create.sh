#!/usr/bin/env bash

docker-compose build --no-cache
docker-compose up -d db && sleep 5
docker-compose stop db
docker-compose run api python manage.py migrate auth
docker-compose run api python manage.py migrate
docker-compose run api python manage.py createsuperuser
