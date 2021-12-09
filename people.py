import sys
from cas.login import CAS
import requests
from datetime import datetime, timedelta

from requests import Session

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

webvpnUrl = "https://web-vpn.sues.edu.cn"
casUrl = "https://cas.sues.edu.cn"

vpnCap = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/captcha.jpg?vpn-1"


def timeGen():  # 上午下午, 2020-01-01, 2020-01-01 10:01
    time_utc = datetime.utcnow()
    time_peking = time_utc + timedelta(hours=8)

    if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    tjsj = time_peking.strftime("%Y-%m-%d")
    return timeType, tjsj


class Person:
    def __init__(self, name: str, pwd: str, liteOCR: bool = False):
        self.name = name
        self.pwd = pwd
        self.__sess = genSess()
        self.cas: CAS = CAS(self.__sess, name, pwd, liteOCR)

    def loginCas(  # 登录cas
        self,
        originUrl: str = casUrl,  # 源url
        openUrl: str = webvpnUrl,  # 要打开的url
        redirectHeader: str = "",  # 重定向前缀
        timeWait: int = 5,  # cas登陆完成后等几秒返回
        encryptedLogin: bool = True,  # 加密登录
    ):
        return self.cas.attachCas(
            originUrl,
            openUrl,
            redirectHeader,
            timeWait=timeWait,
            encryptedLogin=encryptedLogin,
        )

    def login(self):  # 登录vpn
        return self.cas.attachCas(
            originUrl=webvpnUrl, redirectHeader=webvpnUrl, capUrl=vpnCap
        )


def create() -> Person:
    return Person(name=sys.argv[1], pwd=sys.argv[2], liteOCR=False)


def genSess():
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 40
    sess = Session()
    sess.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        }
    )
    return sess
