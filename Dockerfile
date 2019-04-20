FROM python:3.7-alpine
EXPOSE 9001
EXPOSE 9003
ADD . /dev-challenge
WORKDIR /dev-challenge
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip3 install -r requirements.txt