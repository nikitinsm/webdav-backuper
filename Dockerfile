FROM python:2.7

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libxml2-dev libxslt-dev python-dev libcurl4-openssl-dev python-pycurl python-pip
RUN pip install -U pip

# for faster rebuilds
RUN pip install webdavclient

# Install lib
COPY . /repository
WORKDIR /repository
RUN python /repository/setup.py install

WORKDIR /
RUN rm -R /repository

ENTRYPOINT ["webdav-backuper"]