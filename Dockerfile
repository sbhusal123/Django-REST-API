FROM python:3.7-alpine
MAINTAINER suryabhusal

ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# to run the processes inside the docker container
RUN adduser -D surya 
USER surya