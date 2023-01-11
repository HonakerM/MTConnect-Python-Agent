#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Please supply image name and command to run"
    exit 1
fi

image_name=$1

docker run -it --name develop-ctr \
    -e PYPI_USER="${PYPI_USER}" \
    -e PYPI_PASSWORD="${PYPI_PASSWORD}" \
    --rm ${image_name} "${@:2}"