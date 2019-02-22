FROM centos:latest
MAINTAINER github.com/alaypatel07

RUN yum -y update
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python34 python34-setuptools
RUN easy_install-3.4 pip
RUN pip3 install tornado
COPY app.py /
