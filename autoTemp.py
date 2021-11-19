import people
from util.log import log
from util.log import debug, log, debugMode
import util.utils as u
import random
import requests
from datetime import datetime, timedelta

from requests.sessions import Session

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

origin = "https://web-vpn.sues.edu.cn"
vpnPath = "/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1"
tempPath = "/default/work/shgcd/jkxxcj"
tempMainPagePath = "/jkxxcj.jsp"

tempHeader = origin+vpnPath+tempPath
reportUrl = tempHeader+tempPath
lastData = {}


def __queryNear(sess: Session) -> bool:  # 上次填写记录
    sess.headers.update({"referer": reportUrl})

    res = sess.post(
        url=tempHeader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear.biz.ext?vpn-12-o2-workflow.sues.edu.cn",
        verify=False
    )
    near_list = res.json()["resultData"]
    if len(near_list) == 0:
        return False
    else:
        global lastData
        lastData = near_list[0]
        u.lower_json(lastData)
        return True


def __queryToday(sess: Session) -> bool:  # 是否已经填过
    sess.headers.update({"referer": reportUrl})
    ampm, tjsj = __timeGen()
    queryTodayJson = {"params": {'sd': ampm, 'tjsj': tjsj}}

    res = sess.post(
        url=tempHeader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryToday.biz.ext?vpn-12-o2-workflow.sues.edu.cn",
        json=queryTodayJson, verify=False
    )
    today_list = res.json()["resultData"]
    if len(today_list) == 0:
        return False
    else:
        global lastData
        lastData = today_list[0]
        u.lower_json(lastData)
        lastData.pop('id')
        return True


def __submit(sess: Session) -> bool:  # 本次是否填报成功
    global lastData
    lastData["tw"] = str(round(random.uniform(36.3, 36.7), 1))
    updateData = {"params": lastData}
    debug(lastData["gh"] + ",gentemp:" + lastData["tw"])
    finalRes = sess.post(tempHeader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext?vpn-12-o2-workflow.sues.edu.cn",
                         json=updateData, verify=False)
    json = finalRes.json()

    if 'result' not in json:
        log("No result:"+str(json))
        return False
    if json['result']["success"]:
        return True
    else:
        log("Already reported or sever down:"+str(json))
        return False


def report(p: people.Person):  # 是否已经填过, 本次是否成功, 错误信息
    todayOk = False
    try:
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 40
        session = p.login()
        todayOk = __queryToday(session)
        if not todayOk:
            if not __queryNear(session):
                return False, False, p.name+"没填过"
        submitRes = __submit(session)
        return todayOk, submitRes, ""

    except Exception as e:
        if debugMode:
            raise e
        return todayOk, False, str(e)


def __timeGen():  # 上午下午, 2020-01-01, 2020-01-01 10:01
    time_utc = datetime.utcnow()
    time_peking = (time_utc + timedelta(hours=8))

    if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    tjsj = time_peking.strftime("%Y-%m-%d")
    return timeType, tjsj


if __name__ == '__main__':
    todayOk, res, err = report(people.create())
    log("res:"+str(todayOk or res)+",err:"+err)
