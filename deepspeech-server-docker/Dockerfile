FROM ubuntu:18.04

RUN set -x \
        && apt-get update \
        && apt-get upgrade -y

RUN apt-get update

RUN set -x \
        && apt-get install -y apt-transport-https ca-certificates git vim sudo htop curl wget mesa-utils \
        && apt-get install -y software-properties-common libnss3 dirmngr gnupg2 lsb-release tmux apt-utils \
        && rm -rf /var/lib/apt/lists/*

# Setup so that no password is needed when sudoing
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update

RUN apt-get install -y sudo curl python3 python3-pip ffmpeg

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.1/deepspeech-0.6.1-models.tar.gz

RUN mkdir models

RUN tar xvf deepspeech-0.6.1-models.tar.gz -C models --strip-components=1

COPY . .

EXPOSE 80

ENTRYPOINT /usr/bin/python3 /server.py && /bin/bash
