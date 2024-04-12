#!/bin/bash
set -euo pipefail

#docker_host=$DOCKER_HOST
#export DOCKER_HOST=$(cat local/docker_host.txt)

echo '>>> Nginx logs:'
docker service logs gn_nginx --since 60s -t
printf "\n\n>>> Gunicorn logs:"
docker service logs gn_gunicorn --since 60s -t
