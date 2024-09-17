import logging
import os
import time
import requests
import json
import random
import string
import hashlib
from requests import RequestException
from urllib.parse import urlencode, quote
import concurrent.futures

import logging
import logging.handlers
from queue import Queue
host = 'https://acs.m.goofish.com'

ck = ''

def setup_logging(queue):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.handlers.QueueHandler(queue)
    root_logger.addHandler(handler)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    listener = logging.handlers.QueueListener(queue, console_handler)
    listener.start()
    return listener



def log_account_action(account_number, message):
    logging.info(f"🐂🍺账号 {account_number + 1}: {message}")


def generate_random_string(length=50):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_ck_usid(ck1):
    key_value_pairs = ck1.split(";")
    for pair in key_value_pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            if key == "USERID":
                return value
        else:
            print(f"❎错误的 Cookie 格式: {pair}")
    return '账号'


def tq(txt):
    try:
        txt = txt.replace(" ", "")
        txt = txt.replace("chushi;", "")
        txt = txt.replace("zhuli", "")
        pairs = txt.split(";")[:-1]
        ck_json = {}
        for i in pairs:
            ck_json[i.split("=")[0]] = i.split("=")[1]
        return ck_json
    except Exception as e:
        print(f'❎Cookie解析错误: {e}')
        return {}


def xsign(api, data, uid, sid, wua, v):
    body = {
        "data": data,
        "api": api,
        "pageId": '',
        "uid": uid,
        'sid': sid,
        "deviceId": '',
        "utdid": '',
        "wua": wua,
        'ttid': '1551089129819@eleme_android_10.14.3',
        "v": v
    }

    try:
        r = requests.post(
            "http://127.0.0.1:18848/api/getXSign",
            json=body
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f'❎请求签名服务器失败: {e}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'❎请求签名服务器错误: {e}')
        return None


def req(api, data, uid, sid, wua='False', v="1.0"):
    try:
        if type(data) == dict:
            data = json.dumps(data)
        wua = str(wua)
        sign = xsign(api, data, uid, sid, wua, v)
        url = f"{host}/gw/{api}/{v}/"
        headers = {
            "x-sgext": quote(sign.get('x-sgext')),
            "x-sign": quote(sign.get('x-sign')),
            'x-sid': sid,
            'x-uid': uid,
            'x-pv': '6.3',
            'x-features': '1051',
            'x-mini-wua': quote(sign.get('x-mini-wua')),
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'x-t': sign.get('x-t'),
            'x-extdata': 'openappkey%3DDEFAULT_AUTH',
            'x-ttid': '1551089129819@eleme_android_10.14.3',
            'x-utdid': '',
            'x-appkey': '24895413',
            'x-devid': '',
        }

        params = {"data": data}
        if 'wua' in sign:
            params["wua"] = sign.get('wua')

        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                res = requests.post(url, headers=headers, data=params, timeout=5)
                return res
            except requests.exceptions.Timeout:
                print("❎接口请求超时")
            except requests.exceptions.RequestException as e:
                print(f"❎请求异常: {e}")
            retries += 1
            print(f"❎重试次数: {retries}")
            if retries >= max_retries:
                print("❎重试次数上限")
                return None
    except Exception as e:
        print(f'❎请求接口失败: {e}')
        return None


def check_cookie(cookie):
    url = "https://waimai-guide.ele.me/h5/mtop.alsc.personal.queryminecenter/1.0/?jsv=2.6.2&appKey=12574478"
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            cookie_jar = response.cookies
            token = cookie_jar.get('_m_h5_tk', '')
            token_cookie = "_m_h5_tk=" + token
            enc_token = cookie_jar.get('_m_h5_tk_enc', '')
            enc_token_cookie = "_m_h5_tk_enc=" + enc_token
            cookie = hbh5tk(token_cookie, enc_token_cookie, cookie)
            return cookie
        else:
            return None
    except Exception as e:
        print("解析ck错误")
        return None


def tq1(cookie_string):
    """
    获取_m_h5_tk
    """
    if not cookie_string:
        return '-1'
    cookie_pairs = cookie_string.split(';')
    for pair in cookie_pairs:
        key_value = pair.split('=')
        if key_value[0].strip() in ["_m_h5_tk", " _m_h5_tk"]:
            return key_value[1]
    return '-1'


def req1(cookie, api, data_str, v="1.0"):
    try:
        cookie = check_cookie(cookie)
        headers = {
            "authority": "shopping.ele.me",
            "accept": "application/json",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
        }
        timestamp = int(time.time() * 1000)
        # data_str = json.dumps(data)
        token = tq1(cookie)
        token_part = token.split("_")[0]

        sign_str = f"{token_part}&{timestamp}&12574478&{data_str}"
        sign = md5(sign_str)
        url = f"https://guide-acs.m.taobao.com/h5/{api}/{v}/?jsv=2.6.1&appKey=12574478&t={timestamp}&sign={sign}&api={api}&v={v}&type=originaljson&dataType=json"
        data1 = urlencode({'data': data_str})
        r = requests.post(url, headers=headers, data=data1)
        if r:
            return r
        else:
            return None
    except Exception as e:
        return None


def md5(text):
    """
    md5加密
    """
    hash_md5 = hashlib.md5()
    hash_md5.update(text.encode())
    return hash_md5.hexdigest()


def hbh5tk(tk_cookie, enc_cookie, cookie_str):
    """
    合并带_m_h5_tk
    """
    txt = cookie_str.replace(" ", "")
    txt = txt.replace("chushi;", "")
    if txt[-1] != ';':
        txt += ';'
    cookie_parts = txt.split(';')[:-1]
    updated = False
    for i, part in enumerate(cookie_parts):
        key_value = part.split('=')
        if key_value[0].strip() in ["_m_h5_tk", " _m_h5_tk"]:
            cookie_parts[i] = tk_cookie
            updated = True
        elif key_value[0].strip() in ["_m_h5_tk_enc", " _m_h5_tk_enc"]:
            cookie_parts[i] = enc_cookie
            updated = True

    if updated:
        return ';'.join(cookie_parts) + ';'
    else:
        return txt + tk_cookie + ';' + enc_cookie + ';'


class TYT:
    def __init__(self, cki, account_number):
        self.taskId = None
        self.stop = False
        self.gameId = None
        self.token = None
        self.name = None
        self.taskList = None
        self.cki = tq(cki)
        self.uid = self.cki.get("unb")
        self.sid = self.cki.get("cookie2")
        self.name1 = get_ck_usid(cki)
        self.account_number = account_number        

    def login(self, ck):
        api1 = 'mtop.alsc.user.detail.query'
        data1 = json.dumps({})
        try:
            # res1 = req(api1, data1, self.uid, self.sid, "1.0")
            res1 = req1(ck, api1, data1, "1.0")
            if res1.json()['ret'][0] == 'SUCCESS::调用成功':
                self.name = res1.json()["data"]["encryptMobile"]
                api = 'mtop.koubei.interaction.center.common.queryintegralproperty.v2'
                data = json.dumps({"templateIds": "[\"1404\"]"})
                try:
                    # res = req(api, data, self.uid, self.sid, "1.0")
                    res = req1(ck, api, data, "1.0")
                    if res.json()['ret'][0] == 'SUCCESS::调用成功':
                        print(f'[账号{self.account_number}] ✅登录成功,乐园币----[{res.json()["data"]["data"]["1404"]["count"]}]')
                        return True
                    else:
                        if res.json()['ret'][0] == 'FAIL_SYS_SESSION_EXPIRED::Session过期':
                            print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                            return False
                        else:
                            print(f'[{self.name1}] ❌登录失败,原因:{res.text}')
                            return False
                except Exception as e:
                    print(f"[{self.name1}] ❎登录失败: {e}")
                    return False
            else:
                if res1.json()['ret'][0] == 'FAIL_SYS_SESSION_EXPIRED::Session过期':
                    print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                    return False
                else:
                    print(f'[{self.name1}] ❌登录失败,原因:{res1.text}')
                    return False
        except Exception as e:
            print(f"[{self.name1}] ❎登录失败: {e}")
            return False

    def gettoken(self, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps(
            {"bizScene": "CAPYBARA", "bizMethod": "login", "bizParam": "{\"gameId\":\"13254\",\"inviterId\":null}",
             "longitude": "104.09800574183464", "latitude": "30.22990694269538"})
        # res = req(api, data, self.uid, self.sid, "1.0")
        res = req1(ck, api, data, "1.0")
        if res.json()['ret'][0] == 'SUCCESS::调用成功':
            y = json.loads(res.json()["data"]["data"])
            self.token = y["data"]["token"]
            self.gameId = y["data"]["openId"]
            return True
        elif res.json()['ret'][0] == 'FAIL_SYS_SESSION_EXPIRED::Session过期':
            print(f"[{self.name1}] ❎cookie已过期，请重新获取")
            return False
        else:
            print(f'[{self.name1}] ❌获取token失败,原因:{res.text}')
            return False

    # 开始游戏
    def startgame(self):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps({"bizScene": "CAPYBARA", "bizMethod": "startGame",
                           "bizParam": "{\"levelId\":\"1\",\"isRestart\":true,\"gameId\":\"" + self.gameId + "\",\"token\":\"" + self.token + "\"}",
                           "longitude": "105.75325090438128", "latitude": "30.597472842782736"})
        res = req(api, data, self.uid, self.sid, "1.0")

        print("助力: " + res.text)

    ## 菜品类型
    def scdisheslx(self, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps({"bizScene": "CAPYBARA", "bizMethod": "startGame",
                           "bizParam": "{\"levelId\":\"1\",\"isRestart\":false,\"gameId\":\"" + self.gameId + "\"}"})
        try:
            # res = req(api, data, self.uid, self.sid, "1.0")
            res = req1(ck, api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::调用成功':

                a = json.loads(res.json()["data"]["data"])
                if a['data']['levelInfo']['orders']['CusS1001']['foodId'] == '_':
                    foodid = 'Food1001'
                else:
                    foodid = a['data']['levelInfo']['orders']['CusS1001']['foodId']
                foodNum = a['data']['levelInfo']['orders']['CusS1001']['currCount']
                if foodid in a['data']['levelInfo']['currFoods']:
                    if self.scdishes(ck) is not None:
                        if 'currFoods' in a['data']['levelInfo'] and foodid in a['data']['levelInfo']['currFoods']:
                            foodlx = a['data']['levelInfo']['currFoods'][foodid]
                            return foodid, foodNum, foodlx
                        else:
                            print(f"菜品类型错误")
                            return None, None, None
                    else:
                        print(f"菜品类4444型错误")
                        return None, None, None
                else:
                    return 'Food1001', foodNum, 1
            else:
                print(f"[账号{self.account_number}] ❎获取菜品类型失败--{res.text}")
                return None, None, None
        except RequestException as e:
            print(f"[账号{self.account_number}] ❎请求失败: {str(e)}")
            return None, None, None
        except Exception as e:
            logging.exception(f"[账号{self.account_number}] ❎请求失败: {str(e)}")
            return None, None, None

    # 上菜
    def scdishes(self, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps({"bizScene": "CAPYBARA", "bizMethod": "handFoodOut",
                           "bizParam": "{\"levelId\":\"1\",\"handCount\":10,\"gameId\":\"" + self.gameId + "\"}"})
        try:
            # res = req(api, data, self.uid, self.sid, "1.0")
            res = req1(ck, api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::调用成功':
                a = json.loads(res.json()["data"]["data"])
                sysum = a['data']['energy']['num']
                scjg = a['data']['outFoods']
                print(f"[账号{self.account_number}] ✅上菜成功--剩余菜品数量:{sysum}")
                if sysum > 0:
                    return True
                else:
                    print(f"[账号{self.account_number}] ❎上菜失败--菜品数量不足")
                    self.stop = True
                    return False
            else:
                print(f"[账号{self.account_number}] ❎上菜失败--{res.json()['ret'][0]}")
                return None
        except Exception as e:
            print(f"[账号{self.account_number}] ❎2请求失败: {e}")
            return None

    # 提交菜品
    def tjdishes(self, ck):
        foodid, foodNum, foodlx = self.scdisheslx(ck)
        if foodlx is None:
            print(f"[账号{self.account_number}] ❎ 获取菜品信息失败")
            return
        else:
            if foodlx == 0:
                self.scdishes(ck)
            if int(foodNum) < 10:
                api = 'mtop.alsc.playgame.mini.game.dispatch'
                data = json.dumps({
                    "bizScene": "CAPYBARA",
                    "bizMethod": "submitFood",
                    "bizParam": "{\"levelId\":\"1\",\"orderSeatId\":\"CusS1001\",\"foodId\":\"" + foodid + "\",\"foodNum\":\"" + str(
                        foodlx) + "\",\"gameId\":\"" + str(self.gameId) + "\"}"
                })
                try:
                    # res = req(api, data, self.uid, self.sid, "1.0")
                    res = req1(ck, api, data, "1.0")
                    if res.json()['ret'][0] == 'SUCCESS::调用成功':
                        a = json.loads(res.json()["data"]["data"])
                        if a['bizErrorCode'] == 'ORDER_FOOD_ERROR':
                            print(f"[账号{self.account_number}] ❎提交菜品失败--{a['bizErrorMsg']}")
                            self.scdishes(ck)
                        else:
                            print(f"[账号{self.account_number}] ✅提交菜品成功")
                    else:
                        print(f"[账号{self.account_number}] ❎提交菜品失败--{res.json()['ret'][0]}")
                except Exception as e:
                    print(f"[账号{self.account_number}] ❎1请求失败")
            if int(foodNum) >= 10:
                self.scscdishes(ck)

    # 上传菜品
    def scscdishes(self, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps({"bizScene": "CAPYBARA", "bizMethod": "receiveOrderAward",
                           "bizParam": "{\"levelId\":\"1\",\"orderSeatId\":\"CusS1001\",\"gameId\":\"" + self.gameId + "\"}"})
        try:
            # res = req(api, data, self.uid, self.sid, "1.0")
            res = req1(ck, api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::调用成功':
                # print(res.json())
                print(f"[账号{self.account_number}] ✅上传菜品成功")
            else:
                print(f"[账号{self.account_number}] ❎上传菜品失败--{res.json()['ret'][0]}")
        except Exception as e:
            print(f"[账号{self.account_number}] ❎1请求失败: {e}")

    def task(self, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps({"bizScene": "CAPYBARA", "bizMethod": "getTasks",
                           "bizParam": "{\"gameId\":\"" + self.gameId + "\",\"token\":\"" + self.token + "\"}",
                           "longitude": "104.09800574183464", "latitude": "30.22990694269538"})

        # res = req(api, data, self.uid, self.sid, "1.0")
        res = req1(ck, api, data, "1.0")

        if res.json()['ret'][0] == 'SUCCESS::调用成功':
            self.taskList = json.loads(res.json()["data"]["data"])
            return True

    def checkTask(self, ck):
        self.task(ck)
        if 'T001' in self.taskList['data']['tasks']:
            if self.taskList['data']['tasks']['T001']['isFinishe'] == True:
                print(f"[账号{self.account_number}] ✅任务T001已完成")
            elif self.taskList['data']['tasks']['T001']['progress'] == 30:
                print(f"[账号{self.account_number}] 尝试领取 T001 奖励")
                id = self.taskList['data']['tasks']['T001']['taskId']
                if not self.postTask(id, ck):
                    return 'T001'
            else:
                print(f"[账号{self.account_number}] T001 任务未完成！开始做任务⚠️⚠️")
                return 'T001'
        else:
            print(f"[账号{self.account_number}] T001 任务未开始！开始做任务⚠️⚠️")
            return 'T001'

        if 'T002' in self.taskList['data']['tasks']:
            if self.taskList['data']['tasks']['T002']['isFinishe'] == True:
                print(f"[账号{self.account_number}] ✅任务T002已完成")
            elif self.taskList['data']['tasks']['T002']['progress'] == 200:
                print(f"[账号{self.account_number}] 尝试领取 T002 奖励")
                id = self.taskList['data']['tasks']['T002']['taskId']
                if not self.postTask(id, ck):
                    return 'T002'
            else:
                print(f"[账号{self.account_number}] T002 任务未完成！开始做任务⚠️⚠️")
                return 'T002'
        else:
            print(f"[账号{self.account_number}] T002 任务未开始！开始做任务⚠️⚠️")
            return 'T002'

        if 'T003' in self.taskList['data']['tasks']:
            if self.taskList['data']['tasks']['T003']['isFinishe'] == True:
                print(f"[账号{self.account_number}] ✅任务T003已完成！")
            elif self.taskList['data']['tasks']['T003']['progress'] == 2:
                print(f"[账号{self.account_number}] 尝试领取 T003 奖励")
                id = self.taskList['data']['tasks']['T003']['taskId']
                if not self.postTask(id, ck):
                    return 'T003'
            else:
                print(f"[账号{self.account_number}] T003 任务未完成！开始做任务⚠️⚠️")
                return 'T003'
        else:
            print(f"[账号{self.account_number}] T003 任务未开始！开始做任务⚠️⚠️")
            return 'T003'

        return True

    def postTask(self, taskId, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = json.dumps({"bizScene": "CAPYBARA", "bizMethod": "finisheTask",
                           "bizParam": "{\"taskId\":\"" + taskId + "\",\"gameId\":\"" + self.gameId + "\",\"token\":\"" + self.token + "\"}",
                           "longitude": "104.09800574183464", "latitude": "30.22990694269538"})

        # res = req(api, data, self.uid, self.sid, "1.0")
        res = req1(ck, api, data, "1.0")
        print(f"完成任务{taskId}")
        if res.json()['ret'][0] == 'SUCCESS::调用成功':
            # print(res.json())
            nested_data = json.loads(res.json()['data']['data'])
            reward_items = nested_data['data']['rewardItems']
            if reward_items:
                reward_num = reward_items[0]['num']
                print(f"[账号{self.account_number}] ✅完成任务获得乐园币--[{reward_num}]")
                return True
            return False
        return False

    def daoju(self, count, ck):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        bizParam = json.dumps({
            "levelId": "1",
            "itemId": f"It100{random.randint(1, 3)}",
            "removeFoods": {
                "Food1003": random.randint(1, 10),
                "Food1002": random.randint(1, 10),
                "Food1004": random.randint(1, 3)
            },
            "gameId": self.gameId,
            "token": self.token,
        })
        data = json.dumps({
            "bizScene": "CAPYBARA",
            "bizMethod": "useGameProp",
            "bizParam": bizParam,
            "longitude": "104.09800574183464",
            "latitude": "30.22990694269538"
        })
        try:
            # res = req(api, data, self.uid, self.sid, "1.0")
            res = req1(ck, api, data, "1.0")
            # print(res.json())
            if json.loads(res.json()['data']['data'])['bizErrorCode'] == 'OK':
                print(f"[账号{self.account_number}] ✅第{count}次使用道具成功！")
                count = count + 1
                return count
            else:
                print(f'[账号{self.account_number}] ❎第{count}次使用道具失败！！！')
                return count
        except Exception as e:
            print(f"[账号{self.account_number}] ❎1请求失败，结束使用道具: {e}")
            return 6



    def main(self, ck):
        if self.login(ck):
            self.gettoken(ck)
            checkRes = self.checkTask(ck)  

            if checkRes != True:
                print(f"----尝试领取游戏次数----")
                while True and self.stop == False:
                    self.tjdishes(ck)

                print(f"----获取任务列表----")
                self.task(ck)

                if 'T003' in self.taskList['data']['tasks']:
                    if self.taskList['data']['tasks']['T003']['isFinishe'] == True:
                        print(f"[{self.name}] ✅任务T003已完成")
                    elif self.taskList['data']['tasks']['T003']['progress'] == 2:
                        print(f"[{self.name}] 已使用道具 尝试领取奖励")
                        id = self.taskList['data']['tasks']['T003']['taskId']
                        self.postTask(id,ck)
                    else:
                        print(f"[{self.name}] 未使用道具2次，继续任务")
                        usedCount = 1
                        while usedCount < 3:
                            usedCount = self.daoju(usedCount,ck)
                        id = self.taskList['data']['tasks']['T003']['taskId']
                        self.postTask(id,ck)
                else:
                    usedCount = 1
                    while usedCount < 3:
                        usedCount = self.daoju(usedCount,ck)
                    self.task(ck)
                    self.postTask(self.taskList['data']['tasks']['T003']['taskId'],ck)

                if 'T001' in self.taskList['data']['tasks']:
                    if self.taskList['data']['tasks']['T001']['isFinishe'] == True:
                        print(f"[{self.name}] ✅任务T001已完成")
                    elif self.taskList['data']['tasks']['T001']['progress'] == 30:
                        print(f"[{self.name}] ✅尝试领取 T001 奖励")
                        id = self.taskList['data']['tasks']['T001']['taskId']
                        self.postTask(id,ck)
                    else:
                        print(f"[{self.name}] ❎任务T001未完成，进度{self.taskList['data']['tasks']['T001']['progress']}/30")


                if 'T002' in self.taskList['data']['tasks']:
                    if self.taskList['data']['tasks']['T002']['isFinishe'] == True:
                        print(f"[{self.name}] ✅任务T002已完成")
                    elif self.taskList['data']['tasks']['T002']['progress'] == 200:
                        print(f"[{self.name}] ✅尝试领取 T002 奖励")
                        id = self.taskList['data']['tasks']['T002']['taskId']
                        self.postTask(id,ck)
                    else:
                        print(f"[{self.name}] ❎任务 T002 未完成，进度{self.taskList['data']['tasks']['T002']['progress']}/200")
            
            else:
                print(f"[{self.name}] ✅任务已全部完成。")
                

if __name__ == '__main__':
    queue = Queue()
    listener = setup_logging(queue)  

    if 'elmck' in os.environ:
        cookie = os.environ.get('elmck')
    else:
        log_account_action(-1, "环境变量中不存在[elmck],启用本地变量模式")
        cookie = ck
    if cookie == "":
        log_account_action(-1, "本地变量为空，请设置其中一个变量后再运行")
        exit(-1)

    cookies = cookie.split("&")
    log_account_action(-1, f"饿了么共获取到 {len(cookies)} 个账号")

   
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(TYT(ck, i + 1).main, ck): i + 1 for i, ck in enumerate(cookies)} 

        for future in concurrent.futures.as_completed(futures):
            account_number = futures[future]
            try:
                stop = future.result()  
                log_account_action(account_number, "执行完毕")
            except Exception as e:
                log_account_action(account_number, f"执行出错: {e}")

    listener.stop()
