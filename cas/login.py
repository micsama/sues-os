import math
import time
import lxml
from requests.sessions import Session
from bs4 import BeautifulSoup

from util.log import debug

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"
webvpnUrl = "https://web-vpn.sues.edu.cn"
casUrl = "https://cas.sues.edu.cn"

casCap = "https://cas.sues.edu.cn/cas/captcha.jpg"


class CAS:
    def __init__(self, sess: Session, name: str, pwd: str, liteOCR: bool = False):
        self.name = name
        self.pwd = pwd
        self.liteOCR = liteOCR
        self.__sess: Session = sess

    def __genRSAPasswd(self, passwd: str, e: str, m: str):
        m = int.from_bytes(bytearray.fromhex(m), byteorder="big")
        e = int.from_bytes(bytearray.fromhex(e), byteorder="big")
        plaintext = passwd[::-1].encode("utf-8")
        input_nr = int.from_bytes(plaintext, byteorder="big")
        crypted_nr = pow(input_nr, e, m)
        keylength = math.ceil(m.bit_length() / 8)
        crypted_data = crypted_nr.to_bytes(keylength, byteorder="big")
        return crypted_data.hex()

    def attachCas(
        self,
        originUrl: str = casUrl,  # 源url
        openUrl: str = webvpnUrl,  # 要打开的url
        redirectHeader: str = "",  # 重定向前缀
        capUrl: str = casCap,  # 验证码url
        timeWait: int = 5,  # cas登陆完成后等几秒返回
        encryptedLogin: bool = True,  # 加密登录, 强烈不推荐非加密
    ):
        sess = self.__sess
        sess.headers.update({"origin": originUrl})

        # 打开网页
        res = sess.get(openUrl, verify=False)
        history = res.history
        realUrl = openUrl
        if len(history) > 0:
            realUrl = redirectHeader + history[len(history) - 1].headers["location"]
        debug("redirect:" + str(len(history) > 0) + ",realUrl:" + realUrl)
        soup = BeautifulSoup(res.content, "lxml")

        # 找到登录按钮的事件
        res = sess.get(realUrl, verify=False)
        execution = soup.find("input", {"name": "execution"}).attrs["value"]
        postTarget = originUrl + soup.find("form")["action"]

        success = False
        i = 0
        while i < 5:
            valid = False
            i += 1
            j = 0
            while (not valid) and (j < 15):
                j += 1
                if self.liteOCR:
                    from cas.cas_ocr import cas_ocr_url

                    cap, valid = cas_ocr_url(sess, url=capUrl), True
                else:
                    from util.ocr import ocrUrl

                    cap, valid = ocrUrl(sess, url=capUrl)
            data = {
                "username": self.name,
                "authcode": cap,
                "execution": execution,
                "encrypted": "true" if encryptedLogin else "false",
                "_eventId": "submit",
                "loginType": "1",
                "submit": "登 录",
                "password": self.__genRSAPasswd(self.pwd, rsa_e, rsa_m)
                if encryptedLogin
                else self.pwd,
            }
            res = sess.post(postTarget, data, verify=False)
            if realUrl != res.url:
                success = True
                break
        if success:
            time.sleep(timeWait)
            return sess
        else:
            raise Exception("登不上去")
