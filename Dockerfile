FROM python:3.7-alpine
EXPOSE 9001
ADD . /dev-challenge
WORKDIR /dev-challenge
RUN pip3 install -r requirements.txt