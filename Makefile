
IMAGE_NAME?=mtconnect-python
build:
	docker build --tag ${IMAGE_NAME} .

develop: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} bash

run: build
	./scripts/run_container.sh ${IMAGE_NAME} bash

test: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/test_package.sh

test.format: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/format_package.sh --check


format: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/format_package.sh


lint: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/lint_package.sh 

PYPI_USER?=${PYPI_USER}
PYPI_PASSWORD?=${PYPI_PASSWORD}
publish: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/publish_package.sh

# This is only here for completeness. This should only be called via CI
VERSION?=${VERSION}
version: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/set_version.sh ${VERSION}