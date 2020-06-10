# A lightweight version of Docker and runs Python 3.7
# From: https://hub.docker.com/_/python
FROM python:3.7-alpine

# Is optional but you can specify the entity mainting this Image
MAINTAINER Vazkir M B.V.

# Tells Python to run in Unbuffered mode which
# 1) Doesn't alllow Python to buffer outputs and just prints them instead
# 2) Avoids some complications when running the application (not clear?)
ENV PYTHONUNBUFFERED 1

# Copy the requirements.txt from the project into the Docker Image,
# so the docker Image can use it to install the required dependencies.
COPY ./requirements.txt /requirements.txt

# First command to RUN installment of the required dependencies
RUN pip install -r /requirements.txt

# Second  RUN command with setting the WORKDIR and
# COPY’ing the main ./app folder to the Docker Image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Lastly we want to add a USER than is used for running applications only,
# which can me specified by using the “-D” flag
# Why not root?
# -> We’re basically limiting the scope of an attacker which acces our docker container,
# -> by adding another user (compared to root access) which can only run the Application Image.
RUN adduser -D user
USER user
