FROM python:3.6.9-slim

## The MAINTAINER instruction sets the Author field of the generated images
MAINTAINER pablo.arribas100@gmail.com
## DO NOT EDIT THESE 3 lines
RUN mkdir /physionet
COPY ./ /physionet
WORKDIR /physionet

## Install your dependencies here using apt-get etc.

## Do not edit if you have a requirements.txt
RUN pip install -r requirements.txt

