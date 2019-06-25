# How to run it:
# $ docker build --tag web-executor-base --file Dockerfile .
# $ docker run -tih webexec-container-runtime web-executor-base

FROM alpine:latest
MAINTAINER Andrey Kiselev "kiselevandrew@yandex.ru"

RUN adduser --disabled-password --home /home/exec-user  \
            --shell /bin/bash exec-user
RUN apk add --no-cache  \
    python              \
    python3             \
    py-pip              \
    bash
