FROM python:3.8-slim as base

WORKDIR /data

# Install poetry
RUN pip3 install poetry

# Copy depdencies and install base packages
COPY pyproject.toml poetry.lock ./ 
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy rest of the repo
COPY . .
