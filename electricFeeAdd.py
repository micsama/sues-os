# 请前往 https://epay.sues.edu.cn/ 设置支付密码, 否则无法完成校园卡充值
#
# 这玩意需要传入四个参数, 充值未必成功, 因为OCR存在失败概率
# 学号 校园卡密码 充值金额 支付密码
#
# pip install easyocr

import people
import random
from retrying import retry
from requests.sessions import Session
from bs4 import BeautifulSoup
import easyocr
from util.log import debug, log
from util.utils import getStartArgs

__base = 'https://epay.sues.edu.cn'
# 验证码
__code = __base+'/epay/codeimage?'+str(random.randint(1001, 9998))
# 登录
__login = __base+'/epay/j_spring_security_check'
# 查
__bill = __base+'/epay/electric/queryelectricbill'

__prePay = __base+'/epay/electric/load4paidelectricbill'
__realPay = __base+'/epay/electric/payconfirm'
# https://epay.sues.edu.cn/epay/electric/load4paidelectricbill
# elcsysid: 1
# elcarea: 1
# elcbuis: 10
# roomNo: 2015
# dumpEnergy: 161.21
# paidMoney: 0.01
# route:


# <input id="billno" name="billno" type="hidden" value="2c9488a07ce37b3c017"/>
# <input id="refno" name="refno" type="hidden" value="202111282222"/>

# https://epay.sues.edu.cn/epay/electric/payconfirm

# billno: 2c9488a07ce37b3c017
# refno: 20211128222
# status: 0
# banktype:
# paypwd: input!


__elecItem = {
    "sysid": '1',  # 校区: 1 正常公寓, 2 长宁校区, 3 研究生公寓
    "elcarea": "1",  # 四期1, 三期2
    "elcbuis": "10",  # 这是楼id 看下方注释找到自己楼的id
    "roomNo": "2015",  # 你宿舍房间号
}


def __getCode(sess: Session) -> str:
    img = sess.get(__code).content
    reader = easyocr.Reader(['en'])
    code = reader.readtext(image=img, detail=0)
    if len(code) < 1:
        return __getCode(sess)
    code = str(code[0]).strip()
    print("验证码 verify code: "+code)
    return code


@retry(
    stop_max_attempt_number=10  # 最大重试次数, 这玩意是很容易失败的
)
def __findNowBill(sess: Session, stuId: str, cardPwd: str) -> str:
    log("正在登录...")
    imgCode = __getCode(sess)
    loginParams = {
        "j_username": stuId,
        "j_password": cardPwd,
        "imageCodeName": imgCode,
    }
    loginRes = sess.post(__login, params=loginParams)
    # debug("登陆:"+str(loginRes.content))

    log("正在查询电费余额...")
    billRes = sess.post(__bill, params=__elecItem)
    log("电费余额(kWh):"+str(billRes.json()['restElecDegree']))
    return str(billRes.json()['restElecDegree'])


def __feeAdd(sess: Session, nowBill: str, addFee: str, payPwd: str):
    log("本次充值金额: "+addFee)
    prePayJson = {
        'elcsysid': int(__elecItem['sysid']),
        'elcarea': int(__elecItem['elcarea']),
        'elcbuis': int(__elecItem['elcbuis']),
        'roomNo': int(__elecItem['roomNo']),
        'dumpEnergy': float(nowBill),
        'paidMoney': float(addFee),
        'route': None,
    }
    log("正在获取订单...")
    prePayRes = sess.post(__prePay, params=prePayJson)
    # debug("订单html:"+str(prePayRes.content))
    soup = BeautifulSoup(prePayRes.content, "lxml")
    billNo = soup.find(id='billno')['value']
    refNo = soup.find(id='refno')['value']
    log('充值中...订单编号:'+str(refNo))

    realPayJson = {
        'billno': billNo,
        'refno': refNo,
        'status': 0,
        'banktype': None,
        'paypwd': payPwd,
    }
    payRes = sess.post(__realPay, params=realPayJson)
    debug(str(payRes.content))


if __name__ == '__main__':
    args = getStartArgs(4)
    stuId, cardPwd, addFee, payPwd = args
    sess = people.genSess()
    nowBill = __findNowBill(sess, stuId, cardPwd)
    addFee = "%.2f" % float(addFee)
    __feeAdd(sess, nowBill, addFee, payPwd)

#
# nowBill = findNowBill(sess)

# log("请输入充值金额(RMB):")
# addFee = "%.2f" % float(input())
# log(addFee)


# 楼栋id列表 buiId就是楼id
# 0: {buiId: "1", buiName: "四期20号楼"}
# 1: {buiId: "2", buiName: "四期21号楼"}
# 2: {buiId: "3", buiName: "四期23号楼"}
# 3: {buiId: "4", buiName: "四期24号楼"}
# 4: {buiId: "5", buiName: "四期27号楼"}
# 5: {buiId: "6", buiName: "四期28号楼"}
# 6: {buiId: "7", buiName: "四期29号楼"}
# 7: {buiId: "8", buiName: "四期30号楼"}
# 8: {buiId: "9", buiName: "四期33号楼"}
# 9: {buiId: "10", buiName: "四期34号楼"}
# 10: {buiId: "11", buiName: "四期35号楼"}
# 11: {buiId: "12", buiName: "四期36号楼"}
# 12: {buiId: "13", buiName: "四期39号楼"}
# 13: {buiId: "14", buiName: "四期40号楼"}
# 14: {buiId: "15", buiName: "四期41号楼"}
# 15: {buiId: "16", buiName: "四期42号楼"}
# 0: {buiId: "17", buiName: "三期10号楼"}
# 1: {buiId: "18", buiName: "三期11号楼"}
# 2: {buiId: "19", buiName: "三期12号楼"}
# 3: {buiId: "20", buiName: "三期13号楼"}
# 4: {buiId: "21", buiName: "三期14号楼"}
# 5: {buiId: "22", buiName: "三期15号楼"}
# 6: {buiId: "23", buiName: "三期16号楼"}
# 7: {buiId: "24", buiName: "三期17号楼"}
# 8: {buiId: "25", buiName: "三期18号楼"}
# 9: {buiId: "26", buiName: "三期19号楼"}
# 10: {buiId: "27", buiName: "三期20号楼"}
# 11: {buiId: "28", buiName: "三期21号楼"}
# 12: {buiId: "29", buiName: "三期22号楼"}
# 13: {buiId: "30", buiName: "三期23号楼"}
# 14: {buiId: "31", buiName: "三期24号楼"}
# 15: {buiId: "32", buiName: "三期25号楼"}
# 16: {buiId: "33", buiName: "三期26号楼"}
