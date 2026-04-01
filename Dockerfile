# Purpose:
#   Docker image definition for running this Django backend in containers.
#
# Connects with:
#   - docker-compose.yml (service runtime command/ports/volume)
#   - requirements.txt (Python dependencies installed into image)
#   - manage.py runserver command used by compose

FROM ubuntu:latest
LABEL authors="AhmadAlali"

ENTRYPOINT ["top", "-b"]

FROM python:3.12-slim

WORKDIR /app
#This sets the working directory inside the container.
COPY requirements.txt .
#This copies your local requirements.txt file into the container’s current directory.
RUN pip install -r requirements.txt
#This runs inside the container during image build.

COPY . .
#This copies the rest of your project files into the container.
