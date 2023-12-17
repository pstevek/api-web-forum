FROM python:3.11.7-alpine3.19

LABEL maintainer="pstevek@gmail.com"

ENV PYTHONUNBUFFERED 1

# Copy dependencies accross
COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /src

WORKDIR /src

# Install dependencies
RUN apk update && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

ENV PATH="/py/bin:$PATH"

# Clean up
RUN rm -rf /tmp && \
    apk del .tmp-build-deps

EXPOSE 8000