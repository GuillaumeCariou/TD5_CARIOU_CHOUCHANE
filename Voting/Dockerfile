FROM python:3.7-alpine3.14

ENV DEV_PACKAGES="\
    build-base \
    #python3-dev \
    #py3-pip \
    "

ENV PYTHON_PACKAGES="paho-mqtt"


RUN apk add --no-cache --virtual build-deps $DEV_PACKAGES \
    && pip install --no-cache-dir $PYTHON_PACKAGES \
    && apk del build-deps

COPY . .

ENTRYPOINT ["python3"]
CMD ["main.py"]
