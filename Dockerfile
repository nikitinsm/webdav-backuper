FROM python:2.7

RUN apt-get install -y libxml2-dev libxslt-dev python-dev libcurl4-openssl-dev python-pycurl python-pip
RUN pip install -U pip
RUN pip install webdavclient

COPY . /repository
RUN python /repository/setup.py

ENTRYPOINT ['webdav-backuper']