FROM python:3.7-alpine
MAINTAINER suryabhusal

ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt

# update the package manager and download package 'postgresql-client'
# without updating the package manager registry
RUN apk add --update --no-cache postgresql-client jpeg-dev

# virtual sets the alias name for dependency.
# After build, dependency can be removed  refering to alias
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

# Remove temporary build dependency 
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# to run the processes inside the docker container
RUN adduser -D surya
RUN chown -R surya:surya /vol/
RUN chmod -R 755 /vol/web
USER surya
