#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Please supply image name and command to run"
    exit 1
fi

image_name=$1

docker run --name run-ctr --rm ${image_name} "${@:2}"