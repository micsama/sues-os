import math
import time
import sys
from util.log import debug
import requests
from datetime import datetime, timedelta

from requests.sessions import Session
from bs4 import BeautifulSoup

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

origin = "https://web-vpn.sues.edu.cn"
casHeader = 'https://cas.sues.edu.cn'


def timeGen():  # 上午下午, 2020-01-01, 2020-01-01 10:01
    time_utc = datetime.utcnow()
    time_peking = (time_utc + timedelta(hours=8))

    if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    tjsj = time_peking.strftime("%Y-%m-%d")
    return timeType, tjsj


class Person:
    def __init__(self, name: str, pwd: str):
        self.name = name
        self.pwd = pwd
        self.__sess: Session = Session()
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 40
        sess = requests.Session()
        sess.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        })

    def __genRSAPasswd(self, passwd: str, e: str, m: str):
        # 别问我为啥rsa加密要这么写，傻逼cas
        # 参考https://www.cnblogs.com/himax/p/python_rsa_no_padding.html
        m = int.from_bytes(bytearray.fromhex(m), byteorder='big')
        e = int.from_bytes(bytearray.fromhex(e), byteorder='big')
        plaintext = passwd[::-1].encode("utf-8")
        input_nr = int.from_bytes(plaintext, byteorder='big')
        crypted_nr = pow(input_nr, e, m)
        keylength = math.ceil(m.bit_length() / 8)
        crypted_data = crypted_nr.to_bytes(keylength, byteorder='big')
        return crypted_data.hex()

    def attachCas(
        self,
        originUrl: str = casHeader,  # 源url
        openUrl: str = origin,  # 要打开的url
        redirectHeader: str = "",  # 重定向前缀
        timeWait: int = 5  # cas登陆完成后等几秒返回
        weakLogin: False # 是否加密登录
    ) -> Session:
        sess = self.__sess
        sess.headers.update({"origin": originUrl})

        # 打开网页
        res = sess.get(openUrl, verify=False)
        history = res.history
        realUrl = openUrl
        if len(history) > 0:
            realUrl = redirectHeader + \
                history[len(history)-1].headers["location"]
        debug("redirect:"+str(len(history) > 0)+",realUrl:"+realUrl)
        soup = BeautifulSoup(res.content, "lxml")

        # 找到登录按钮的事件
        res = sess.get(realUrl, verify=False)
        execution = soup.find("input", {"name": "execution"}).attrs["value"]
        postTarget = originUrl+soup.find("form")["action"]
        if weakLogin:
            data = {
                "username": self.name,
                "password": self.pwd,
                "execution": execution,
                "_eventId": "submit",
                "loginType": "1",
                "submit": "登 录"
            }
        else:
            data = {
                "username": self.name,
                "password": self.__genRSAPasswd(self.pwd, rsa_e, rsa_m),
                "execution": execution,
                "encrypted": "true",
                "_eventId": "submit",
                "loginType": "1",
                "submit": "登 录"
            }

        res = sess.post(postTarget, data, verify=False)
        time.sleep(timeWait)
        return sess

    def login(self) -> Session:  # 登录vpn
        return self.attachCas(originUrl=origin, redirectHeader=origin, weakLogin = False)


def create() -> Person:
    return Person(name=sys.argv[1], pwd=sys.argv[2])
