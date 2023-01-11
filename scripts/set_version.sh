#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Please supply version"
    exit 1
fi

poetry version "$@"