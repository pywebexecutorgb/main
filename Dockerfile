# Python execution environment

# How to run it:
# $ docker build --tag web-executor --file Dockerfile .
# $ docker run -tih webexec-container web-executor

FROM alpine:latest
MAINTAINER Andrey Kiselev "kiselevandrew@yandex.ru"

RUN apk add --no-cache  \
    python              \
    python3             \
    py-pip              \
    bash

CMD /bin/bash
