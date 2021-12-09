# sues-api open source(sues-os)

[![PublicToDokcerHub](https://github.com/SUES-eLib/sues-os/actions/workflows/BuildEnvDocker.yml/badge.svg)](https://github.com/SUES-eLib/sues-os/actions/workflows/BuildEnvDocker.yml)

sues api 开放计划，目前：

1. [electricFeeGet.py](electricFeeGet.py): 电费查询api
2. [electricFeeGetVpn.py](electricFeeGetVpn.py): 电费查询api(通过web-vpn)
3. [electricFeeAdd.py](electricFeeAdd.py): 电费充值api
4. [electricFeeAddVPN.py](electricFeeAdd.py): 电费充值api(通过web-vpn)
5. [blance.py](blance.py): 校园卡余额api
6. [people.py](people.py): 基础CAS登录及web-vpn
7. [autoTemp.py](autoTemp.py) 自动化健康填报

---

## requirements

- python 3.9+
<!-- - [chromedriver](http://chromedriver.storage.googleapis.com/index.html) 下载解压，并将所在目录添加到path -->
<!-- - Node enviromrnt
- python package: -->

Windows:

```bash
pip install torch torchvision torchaudio # if no GPU

pip install -r requirements.txt
# pip install -r requirements-lite.txt(精简依赖, OCR成功率可能会降低)
```

Linux/Mac

```bash
pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html  # if no GPU

pip3 install -r requirements.txt
# pip3 install -r requirements-lite.txt(精简依赖, OCR成功率可能会降低)
```

## 使用

### 本地运行

1. 如果代码注释里面没说的话，一般使用方式: `python xxx.py 学号 密码`, 否则详见代码注释。
2. debug日志输出控制: 位于[util/log.py](util/log.py)

### 在 Docker 中使用 [@dextercai](https://github.com/dextercai)

本项目具备**小而美**的Docker镜像，方便自动化场景使用。您也可以根据项目内dockerfile与WorkFlow自行构建使用。

Docker images:

```text
zsqw123/sues-os-docker //(完整版，nightly，with new feature)
zsqw123/sues-os-docker-temp //(精简版，鲁棒性差，nightly，with new feature)
dextercai/sues-os-env:full //(完整版，stable)
dextercai/sues-os-env:lite //(精简版，stable)
```


> **敬告**：完整Docker将占用您大约`600M+`网络流量，精简版docker只包含基础的cas/vpn/体温填报等功能（鲁棒性较差，体积70M+）

命令行方式:

```bash
docker pull dextercai/sues-os-env:full
docker run -d -it --name="sues-os-env" dextercai/sues-os-env
docker exec -it sues-os-env /bin/bash
//体温填报需使用flags风格的参数设定
python3.9 autoTemp.py --lite 1 --usr 1919810 --pwd 114514 // --lite设为1，使用精简识别模式
python3.9 autoTemp.py --lite 0 --usr 1919810 --pwd 114514 // --lite设为0，使用完整识别模式（仅完整版镜像环境可用）
```

### Build Docker

考虑到DockerHub对免费账户下的镜像存在单位时间内最大拉取量限制，故可以自行利用GithubAction服务进行构建。

如果需要自行构建Docker镜像，请Fork本项目，并在Repo Secrets中妥善配置好`DOCKER_REPO` `DOCKER_USERNAME` `DOCKER_PASSWORD` `DOCKER_REPO_TEMP`即可。

其他私有镜像库推送，请参考对应平台手册资料。
