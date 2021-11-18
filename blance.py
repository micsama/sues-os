from people import Person
from util.log import log


if __name__ == '__main__':
    import sys
    casHeader = 'https://cas.sues.edu.cn'
    targetUrl = "https://mlapp.sues.edu.cn/mobile/getAccountBalance.rst"
    person = Person(name=sys.argv[1], pwd=sys.argv[2])
    sess = person.loginCas(originUrl=casHeader, openUrl=targetUrl)
    res = sess.get(url=targetUrl, verify=False)
    log("校园卡余额还剩："+res.json()['data']['DQYE'])
