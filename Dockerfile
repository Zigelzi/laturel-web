# Pull official base image (Alpine is compact linux distro)
FROM python:3.8.0-alpine

# Set working directory for the application
WORKDIR /usr/src/app

# Set environment variables

# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apk add --no-cache --update python3-dev  gcc build-base
RUN pip install -r requirements.txt

# Copy the project
COPY . /usr/src/app/