import easyocr
from requests.sessions import Session

from util.log import debug, log

reader = easyocr.Reader(["en"])


def __isDigit(s: str):
    return s.isdigit() and len(s) == 4


# 输入: sess, 图片url, judge: 判断是否合法, 默认全是数字合法
# 返回: int:ocrResult, 是否合法验证码
def ocrUrl(sess: Session, url: str, judge=__isDigit):
    resp = sess.get(url)
    ocrRes = ocrBs(resp.content)
    valid = judge(ocrRes)
    log("ocrRes:{} valid:{}".format(ocrRes, valid))
    return ocrRes, valid

# 输入: 图片bytes
# 返回: 验证码识别结果
# 这里可以实现你自己的OCR算法
def ocrBs(bs: bytes) -> str:
    ocrList = reader.readtext(image=bs, detail=0)
    if len(ocrList) == 0:
        return ""
    return str(ocrList[0])