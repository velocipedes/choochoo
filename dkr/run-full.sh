#!/bin/bash

rm docker-compose.yml
ln -s docker-compose-full.yml docker-compose.yml
docker container prune -f
docker-compose up

