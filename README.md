# sues-api open source(sues-os)

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

- python 3.9
<!-- - [chromedriver](http://chromedriver.storage.googleapis.com/index.html) 下载解压，并将所在目录添加到path -->
<!-- - Node enviromrnt
- python package: -->

Windows:

```bash
pip install -r requirements.txt
```

Linux/Mac

```bash
pip3 install -r requirements.txt
```

## use

如果代码注释里面没说的话，一般使用方式:

```bash
python xxx.py 学号 密码
```

否则详见代码注释

## Use In Docker

本项目具备一个基于Fedora Linux的Docker镜像，方便自动化场景使用。您也可以根据项目内dockerfile与WorkFlow自行构建使用。
```
docker pull dextercai/sues-os-env:latest
docker run -d -it --name="sues-os-env" dextercai/sues-os-env
docker exec -it sues-os-env /bin/bash
python3.9 autoTemp.py 114514 1919810
```
