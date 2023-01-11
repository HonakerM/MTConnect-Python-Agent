FROM python:3.8-slim as base

WORKDIR /data

# Install Deps if there are any
COPY pyproject.toml poetry.lock ./
RUN pip3 install poetry && \
    poetry install --only main --no-root

COPY . .
