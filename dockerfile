FROM fedora

LABEL MAINTAINER="dextercai"



#依赖
RUN dnf makecache \
    && dnf install python3.9 -y \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.9 get-pip.py

RUN mkdir /root/sues-os

WORKDIR /root/sues-os
COPY ./ ./

RUN pip3.9 install -r requirements.txt && pip3.9 install lxml

#本项目用到的两个模型识别文件
RUN mkdir -p ~/.EasyOCR/model \
    && dnf install wget -y \
    && wget -O ~/.EasyOCR/model/craft_mlt_25k.pth https://drcai.coding.net/api/team/drcai/anonymity/artifacts/repositories/12214058/packages/3631498/versios/10825970/file/download?fileName=craft_mlt_25k.pth \
    && wget -O ~/.EasyOCR/model/english_g2.pth	https://drcai.coding.net/api/team/drcai/anonymity/artifacts/repositories/12214058/packages/3631497/versions/10825963/file/download?fileName=english_g2.pth

