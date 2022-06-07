#!/bin/bash

docker build -t {{cookiecutter.project_name}}:base -f Dockerfile.base .
docker-compose up -d --build