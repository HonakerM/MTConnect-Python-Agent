
IMAGE_NAME?=mtconnect-python
build:
	docker build --tag ${IMAGE_NAME} .

develop: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} bash

test: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/test_package.sh

format: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/format_package.sh

lint: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/lint_package.sh

PYPI_USER?=${PYPI_USER}
PYPI_PASSWORD?=${PYPI_PASSWORD}
publish: build
	./scripts/run_develop_container.sh ${IMAGE_NAME} scripts/publish_package.sh