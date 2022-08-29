#!/bin/bash

docker build -t {{cookiecutter.project_name}} -f deploy/docker/Dockerfile .
docker-compose -f deploy/docker/docker-compose.yml up -d