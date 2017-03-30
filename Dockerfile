# tlsmd port 8100

FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
ENV APP_DIR /opt/tlsmd

RUN apt-get -y update \
 && apt-get -y install apt-utils \
 && apt-get -y upgrade \
 && apt-get -y install curl git cmake pkg-config python-dev python-virtualenv \
 libcurl4-openssl-dev libyaml-dev libxml2-dev libxslt1-dev libmysqlclient-dev \
 libjpeg-dev zlib1g-dev python-dev libjpeg-dev libfreetype6-dev zlib1g-dev \
 libatlas-base-dev liblapack-dev gfortran libpq-dev swig libffi-dev libboost-all-dev

## done setting up image -- now add app

WORKDIR ${APP_DIR}
COPY . ${APP_DIR}/

RUN ./manage build_all

EXPOSE 8100
CMD ["./manage.sh", "rungu_prod"]
