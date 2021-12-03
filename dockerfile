FROM fedora

LABEL MAINTAINER="dextercai"

RUN dnf makecache \
    && dnf install python3.9 -y \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.9 get-pip.py

RUN mkdir /root/sues-os

WORKDIR /root/sues-os
COPY ./ ./

RUN pip3.9 install -r requirements.txt && pip3.9 install lxml && rm -rf ~/.cache

RUN mkdir -p ~/.EasyOCR/model \
    && dnf install wget -y \
    && wget -O ~/.EasyOCR/model/craft_mlt_25k.pth https://drcai-generic.pkg.coding.net/PersonalDisk/util/craft_mlt_25k.pth?version=latest \
    && wget -O ~/.EasyOCR/model/english_g2.pth	https://drcai-generic.pkg.coding.net/PersonalDisk/util/english_g2.pth?version=latest

