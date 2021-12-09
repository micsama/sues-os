import people
from util.log import log

if __name__ == '__main__':
    targetUrl = "https://mlapp.sues.edu.cn/mobile/getAccountBalance.rst"
    person = people.create()
    sess = person.loginCas(openUrl=targetUrl)
    res = sess.get(url=targetUrl, verify=False)
    log("校园卡余额还剩："+res.json()['data']['DQYE'])
