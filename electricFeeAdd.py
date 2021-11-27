# pip install easyocr

from math import trunc
import people
import random
from requests.sessions import Session
import easyocr
from PIL import Image
from util.log import log

__base = 'https://epay.sues.edu.cn'
# 验证码
__code = __base+'/epay/codeimage?'+str(random.randint(1001, 9998))
# 登录
__login = __base+'/epay/j_spring_security_check'
# 查
__bill = '/epay/electric/queryelectricbill'


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


if __name__ == '__main__':
    sess = people.genSess()
    imgCode = __getCode(sess)
    peo = people.create()
    loginParams = {
        "j_username": peo.name,
        "j_password": peo.pwd,
        "imageCodeName": imgCode,
    }
    sess.post(__login, params=loginParams)


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
