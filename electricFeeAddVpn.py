# electricFeeAdd 的 VPN 版本
# 请务必看 electricFeeAdd.py 的注释！！！！
# ！！！！！！！！
# ！！！！！！
# 不同点是最后要加一个 VPN/CAS 的密码作为传入参数

from util.log import log
from util.utils import getStartArgs
from electricFeeAdd import changeBase, feeAdd, findNowBill
import people

if __name__ == '__main__':
    args = getStartArgs(5)
    changeBase(
        'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f5e7408569237d556d468ca88d1b203b')
    stuId, cardPwd, addFee, payPwd, vpnPwd = args
    sess = people.Person(stuId, vpnPwd).login()
    nowBill = findNowBill(sess, stuId, cardPwd)
    addFee = "%.2f" % float(addFee)
    feeAdd(sess, nowBill, addFee, payPwd)
