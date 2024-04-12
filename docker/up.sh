#!/bin/bash
set -eo pipefail

export DOCKER_BUILDKIT=1

#export DOCKER_HOST=$(cat local/docker_host.txt)
#if [ ! -f "secrets/some-key.txt" ]
#then
#    echo "file 'secrets/some-key.txt' not found" >&2
#    exit 1
#fi

export GUNICORN_ENTRYPOINT_HASH=`md5sum gunicorn-entrypoint.sh | awk '{print $1}'`
export GUNICORN_CONF_HASH=`md5sum gunicorn.conf.py | awk '{print $1}'`
export NGINX_CONF_HASH=`md5sum nginx.conf | awk '{print $1}'`
export SERVER_SETTINGS_HASH=`md5sum server_settings.py | awk '{print $1}'`
export SOME_KEY_HASH=abc
#export SOME_KEY_HASH=`md5sum secrets/some-key.txt | awk '{print $1}'`
cat docker-stack.yml | envsubst '${GUNICORN_ENTRYPOINT_HASH},${GUNICORN_CONF_HASH},${NGINX_CONF_HASH},${SERVER_SETTINGS_HASH},${SOME_KEY_HASH}' > docker-stack.build.yml

if [ "$1" = "--no-build" ]
then
    build=0
fi

if [ "$1" = "--build" ]
then
    build=1
fi

if [ -z "$build" ]
then
    while true; do
        read -p "Rebuild the images? [y/n]" yn
        case $yn in
            [Yy]* ) build=1; break;;
            [Nn]* ) build=0; break;;
            * ) echo "[y/n]";;
        esac
    done
fi

set -u

if [ "$build" -eq 1 ]
then
    cd ../..
    docker build -t hackaton-mipt-digital-24-04/images:gn -f gn/docker/gunicorn.Dockerfile .
    cd gn/docker
fi

if ! docker stack ls &>/dev/null
then
    # todo advertise addr
    docker swarm init
fi
docker stack up --detach=false -c docker-stack.build.yml gn

if [ "$build" -eq 1 ]
then
    docker service update --image nginx:1.24.0-alpine gn_nginx
    docker service update --force gn_nginx
    docker service update --image hackaton-mipt-digital-24-04/images:gn gn_gunicorn
    docker service update --force gn_gunicorn
fi

#docker secret ls | grep -E "\bgn_some-key_[a-f0-9]{32}\b" | grep -v -E "\bgn_some-key_$SOME_KEY_HASH\b" | awk '{print $1}' | xargs -r docker secret rm
docker config ls | grep -E "\bgn_gunicorn-entrypoint_[a-f0-9]{32}\b" | grep -v -E "\bgn_gunicorn-entrypoint_$GUNICORN_ENTRYPOINT_HASH\b" | awk '{print $1}' | xargs -r docker config rm
docker config ls | grep -E "\bgn_gunicorn-conf_[a-f0-9]{32}\b" | grep -v -E "\bgn_gunicorn-conf_$GUNICORN_CONF_HASH\b" | awk '{print $1}' | xargs -r docker config rm
docker config ls | grep -E "\bgn_nginx-conf_[a-f0-9]{32}\b" | grep -v -E "\bgn_nginx-conf_$NGINX_CONF_HASH\b" | awk '{print $1}' | xargs -r docker config rm
docker config ls | grep -E "\bgn_sever-settings_[a-f0-9]{32}\b" | grep -v -E "\bgn_sever-settings_$SERVER_SETTINGS_HASH\b" | awk '{print $1}' | xargs -r docker config rm
