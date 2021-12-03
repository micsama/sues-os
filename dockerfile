FROM frolvlad/alpine-glibc:alpine-3.14

LABEL MAINTAINER="dextercai"
ARG CONDA_DIR="/opt/conda"

ENV PATH="$CONDA_DIR/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

#安装MiniConda
RUN apk add --no-cache --virtual .build-dependencies bash ca-certificates wget && \
    mkdir -p "$CONDA_DIR" && \
    wget "http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" -O miniconda.sh && \
    bash miniconda.sh -f -b -p "$CONDA_DIR" && \
    echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
    conda update --all --yes && \
    conda config --set auto_update_conda False && \
    apk del --purge .build-dependencies && \
    rm -f miniconda.sh && \
    conda clean --all --force-pkgs-dirs --yes && \
    find "$CONDA_DIR" -follow -type f \( -iname '*.a' -o -iname '*.pyc' -o -iname '*.js.map' \) -delete && \
    mkdir -p "$CONDA_DIR/locks" && \
    chmod 777 "$CONDA_DIR/locks"

RUN mkdir /root/sues-os

WORKDIR /root/sues-os

COPY ./ ./

#依赖
RUN pip install -r requirements.txt

#本项目用到的两个模型识别文件
RUN mkdir -p ~/.EasyOCR/model \
    && wget -O ~/.EasyOCR/model/craft_mlt_25k.pth https://drcai.coding.net/api/team/drcai/anonymity/artifacts/repositories/12214058/packages/3631498/versios/10825970/file/download?fileName=craft_mlt_25k.pth \
    && wget -O ~/.EasyOCR/model/english_g2.pth	https://drcai.coding.net/api/team/drcai/anonymity/artifacts/repositories/12214058/packages/3631497/versions/10825963/file/download?fileName=english_g2.pth

