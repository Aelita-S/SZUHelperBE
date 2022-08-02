# Dockerfile
FROM python:3.8-alpine

ENV PROJ_ENV PROD

ADD . /app
WORKDIR /app

#HEALTHCHECK --interval=5s --retries=3 CMD python2 /app/deploy/health_check.py

RUN apk update --no-cache && \
    apk add --no-cache --virtual .build-deps build-base libffi-dev python3-dev libc-dev zlib-dev && \
    apk add --no-cache libxslt-dev postgresql-dev supervisor openssh privoxy autossh && \
    pip install --no-cache-dir -r /app/.deploy/requirements.txt && \
    apk del .build-deps --purge

ENTRYPOINT ["sh", "/app/.deploy/entrypoint.sh"]
