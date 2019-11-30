FROM python:3.7-alpine
MAINTAINER suryabhusal

ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt

# update the package manager and download package 'postgresql-client'
# without updating the package manager registry
RUN apk add --update --no-cache postgresql-client

# virtual sets the alias name for dependency.
# After build, dependency can be removed  refering to alias
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# Remove temporary build dependency 
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# to run the processes inside the docker container
RUN adduser -D surya
USER surya
