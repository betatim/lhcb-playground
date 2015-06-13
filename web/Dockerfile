# web server part of the LHCb playground

FROM ubuntu:14.10

MAINTAINER Tim Head <betatim@gmail.com>

# XXX How much of this is needed with miniconda?

RUN apt-get update && apt-get upgrade -y && apt-get install python-pip python python-dev libcurl4-openssl-dev -y
RUN pip install --upgrade pip

EXPOSE 7777

RUN useradd -m -s /bin/bash another
USER another
ENV HOME /home/another
ENV SHELL /bin/bash
ENV USER another
WORKDIR $HOME

ADD . $HOME/web

ENV DOCKER_HOST unix://docker.sock

RUN pip install --user -r web/requirements.txt

CMD python web/orchestrate.py