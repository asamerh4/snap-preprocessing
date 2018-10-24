FROM centos

MAINTAINER Hubert Asamer

RUN yum -y update && yum -y install epel-release && yum -y update && yum -y install python-pip jq java gdal gdal-python && pip install --upgrade pip  && pip install awscli certifi

COPY tools/snap-bundle /root/tools/snap-bundle
COPY tools/snap-config/snap.auxdata.properties /root/.snap/etc/snap.auxdata.properties
COPY tools/snap-graphs/s1-calibration.xml.template /root/s1-calibration.xml.template
COPY tools/runner/s1-calibrate-warp.py /root/s1-calibrate-warp.py
WORKDIR /root

