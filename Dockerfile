# Purpose:
#   Build a simple image for running this Django project.
#
# Connects with:
#   - requirements.txt for dependency installation
#   - docker-compose.yml for runtime command/network/env wiring

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
