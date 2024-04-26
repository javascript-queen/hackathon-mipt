#!/bin/bash
set -e

#docker_host=$DOCKER_HOST
#export DOCKER_HOST=$(cat conf/docker_host.txt)

docker stack down gn
