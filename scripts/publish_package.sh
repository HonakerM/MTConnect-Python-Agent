#!/bin/bash

poetry build
poetry publish --username "${PYPI_USER}" --password "${PYPI_PASSWORD}"