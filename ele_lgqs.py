# -*- coding: utf-8 -*-

import hashlib
import os
import re
import time
import requests
from urllib.parse import urlencode, quote
import execjs
import tempfile
import subprocess

host = 'https://acs.m.goofish.com'

ck = ''

import json
import random
import string
import base64  

def rsa_encrypt(public_key_pem, data_str):
    url = 'http://mzkj666.cn:9324/encrypt'
    data = {
        'publicKeyPem': public_key_pem,
        'dataStr': data_str
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['encryptedData']
    else:
        return response.json()['encryptedData']

def generate_random_string(length=50):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_ck_usid(ck1):
    key_value_pairs = ck1.split(";")
    for pair in key_value_pairs:
        key, value = pair.split("=")
        if key == "USERID":
            return value
        else:
            return '账号'

def hbh5tk(tk_cookie, enc_cookie, cookie_str):
    """
    合并带_m_h5_tk
    """
    txt = cookie_str.replace(" ", "")
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


def tq(cookie_string):
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


def tq1(txt):
    """
    拆分cookie
    """
    try:
        txt = txt.replace(" ", "")
        if txt[-1] != ';':
            txt += ';'
        pairs = txt.split(";")[:-1]
        ck_json = {}
        for pair in pairs:
            key, value = pair.split("=", 1)
            ck_json[key] = value
        return ck_json
    except Exception as e:
        print(f'❎Cookie解析错误: {e}')
        return {}


def md5(text):
    """
    md5加密
    """
    hash_md5 = hashlib.md5()
    hash_md5.update(text.encode())
    return hash_md5.hexdigest()


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

class TYT:
    def __init__(self, cki):
        self.name = None
        self.ck = cki
        self.cki = tq1(cki)
        self.uid = self.cki.get("unb")
        self.sid = self.cki.get("cookie2")
        self.name1 = get_ck_usid(cki)
        self.curGameId = ""
        self.propertyId = ""
        self.gamePublicKey = ""
        self.gameCount = 0

    def xsign(self, api, data, wua, v):
        body = {
            "data": data,
            "api": api,
            "pageId": '',
            "uid": self.uid,
            'sid': self.sid,
            "deviceId": '',
            "utdid": '',
            "wua": wua,
            'ttid': '1551089129819@eleme_android_10.14.3',
            "v": v
        }

        try:
            r = requests.post(
                "http://192.168.1.124:1888/api/getXSign",
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

    def xsign_req(self, api, data, wua='False', v="1.0"):
        try:
            if type(data) == dict:
                data = json.dumps(data)
            wua = str(wua)
            sign = self.xsign(api, data, wua, v)
            url = f"{host}/gw/{api}/{v}/"
            headers = {
                "x-sgext": quote(sign.get('x-sgext')),
                "x-sign": quote(sign.get('x-sign')),
                'x-sid': self.sid,
                'x-uid': self.uid,
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

    def no_xsign_req(self, api, data, v="1.0"):
        try:
            cookie = check_cookie(self.ck)
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
            data_str = json.dumps(data)
            token = tq(cookie)
            token_part = token.split("_")[0]

            sign_str = f"{token_part}&{timestamp}&12574478&{data_str}"
            sign = md5(sign_str)
            url = f"https://guide-acs.m.taobao.com/h5/{api}/{v}/?jsv=2.6.1&appKey=12574478&t={timestamp}&sign={sign}&api={api}&v={v}&type=originaljson&dataType=json"
            data1 = urlencode({'data': data_str})
            r = requests.post(url, headers=headers, data=data1)
            if r.json()['ret'][0] in ['SUCCESS::接口调用成功','SUCCESS::调用成功']:
                return r
            else:
                # print('请求失败：',r.text)
                return f"请求异常：{r.json()['ret'][0]}"
        except Exception as e:
            print('请求出现错误：',e)
            return None

    def login(self):
        api1 = 'mtop.alsc.user.detail.query'
        data1 = {}
        try:
            res1 = self.no_xsign_req(api1, data1, "1.0")
            if res1.json()['ret'][0] == 'SUCCESS::调用成功':
                self.name = res1.json()["data"]["encryptMobile"]
                api = 'mtop.koubei.interaction.center.common.queryintegralproperty.v2'
                data = {"templateIds": "[\"1404\"]"}
                try:
                    res = self.no_xsign_req(api, data, "1.0")
                    if res.json()['ret'][0] == 'SUCCESS::调用成功':
                        print(f'[{self.name}] ✅登录成功,乐园币----[{res.json()["data"]["data"]["1404"]["count"]}]')
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
    
    def task(self):
        print(f"[{self.name1}] 开始获取游戏任务")
        api = 'mtop.ele.biz.growth.task.core.querytask'
        data = json.dumps({"bizScene": "BLUE_KNIGHT_PARKOUR", "accountPlan": "HAVANA_COMMON", "missionCollectionId": "1322",
                           "locationInfos": "[\"{\\\"lng\\\":\\\"120.220572\\\",\\\"lat\\\":\\\"30.178625\\\"}\"]"
                           })
        try:
            res = self.xsign_req(api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::接口调用成功':
                if res.json()["data"]["mlist"][0]["stage"]['count'] < 5:
                    count = 5 - int(res.json()["data"]["mlist"][0]["stage"]['count'])
                    for _ in range(int(count)):
                        api = 'mtop.ele.biz.growth.task.event.pageview'
                        data = {
                            "collectionId": "1322",
                            "missionId": "23414001",
                            "actionCode": "PAGEVIEW",
                            "pageFrom": "a2ogi.bx1157100",
                            "viewTime": "15",
                            "bizScene": "BLUE_KNIGHT_PARKOUR",
                            "accountPlan": "KB_ORCHARD",
                            "sync": "false",
                            "asac": "2A23C08X4VP4SVOKFBKCA9",
                        }
                        try:
                            res1 = self.no_xsign_req(api, data, "1.0")
                            if res1:
                                if '异常' not in res1:
                                    print(f'[{self.name}] ✅任务完成成功！')
                                else:
                                    print(f'[{self.name}] ✅任务完成出错：',res1)
                                    break
                            else:
                                print(f'[{self.name}] ✅任务完成失败：',res1)
                        except Exception as e:
                            print(f"[{self.name}] ❎请求失败：",e)
                            return None
        except Exception as e:
            print(f"[{self.name}] ❎请求失败1")

        print(f"[{self.name1}] 开始获取可领取次数")
        api = 'mtop.ele.biz.growth.task.core.querytask'
        data = json.dumps({
            "bizScene": "BLUE_KNIGHT_PARKOUR",
            "accountPlan": "HAVANA_COMMON",
            "missionCollectionId": "1322",
            "locationInfos": "[\"{\\\"lng\\\":\\\"120.220572\\\",\\\"lat\\\":\\\"30.178625\\\"}\"]"
        })
        try:
            res = self.xsign_req(api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::接口调用成功':
                for y in res.json()['data']['mlist']:
                    for o in y['missionStageDTOS']:
                        if o['rewardStatus'] == "TODO" and o['status'] == "FINISH":
                            if o['rewards'][0]['name'] == "次数":
                                api1 = 'mtop.ele.biz.growth.task.core.receiveprize'
                                data1 = {"bizScene": "BLUE_KNIGHT_PARKOUR", "missionCollectionId": "1322", "missionId": "23414001",
                                     "locationInfos": "[\"{\\\"lng\\\":\\\"105.754353\\\",\\\"lat\\\":\\\"30.600449\\\"}\"]",
                                     "accountPlan":"HAVANA_COMMON",
                                     "count": o['stageCount'],
                                       "asac": "2A23B18B2HYMDVFDDOXP2F"}
                                try:
                                    res1 = self.no_xsign_req(api1, data1, "1.0")
                                    if (res1 is None) or (res1 and '异常' in res1):
                                        continue
                                    data = res1.json()["data"]
                                    if data.get('errorMsg') is not None:
                                        print(f"[{self.name}] ❎领取奖励失败: {data['errorMsg']}")
                                    else:
                                        rlist = data.get('rlist')
                                        if rlist is not None:
                                            print(f"[{self.name}] ✅领取游戏次数成功--{rlist[0]['value']}次")
                                        else:
                                            print(f"[{self.name}] ❎{res1.json()['ret'][0]}")
                                except Exception:
                                    print(f'请求错误')
                                    return None
        except Exception as e:
            print(f"[{self.name}] ❎请求失败：",e)    

    def query_game_info(self):
        api = 'mtop.alsc.playgame.mini.game.index'
        data = json.dumps({
            "bizScene": "BLUE_KNIGHT_PARKOUR",
            "latitude": "30.17862595617771",
            "longitude": "120.22057268768549",
            "collectionIds": "[\"20240204214413721933320869\"]",
            "actId": "20240204214413716190833090"
        })
        try:
            res = self.xsign_req(api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::调用成功':
                if len(res.json()["data"]["data"]['propertyList']):
                    for propertyItem in res.json()["data"]["data"]['propertyList']:
                        if propertyItem['propertyName'] == '乐园币':
                            print(f'[{self.name}] ✅乐园币----[{propertyItem["amount"]}]')
                            self.propertyId = propertyItem['propertyId']
                        elif propertyItem['propertyName'] == '剩余奖励次数':
                            self.gameCount = int(propertyItem['amount'])
                            print(f'[{self.name}] ✅剩余游戏次数----[{propertyItem["amount"]}]')
            else:
                print(f"[{self.name}] ❌查询游戏信息失败,原因:{res.text}")
        except Exception as e:
            print(f"[{self.name}] ❎查询游戏信息失败")

    def start_game(self):
        api = 'mtop.alsc.playgame.mini.game.play.start'
        data = json.dumps({
            "bizScene":"BLUE_KNIGHT_PARKOUR",
            "latitude": "30.17862595617771",
            "longitude": "120.22057268768549",
            "actId":"20240204214413716190833090",
            "gamePattern":"REWARD_PATTERN",
            "extParams":"{\"changeVersion\":\"20240412\"}"
            })
        try:
            res = self.xsign_req(api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::调用成功':
                if res.json()["data"]["data"]['curGameId']:
                    self.curGameId = res.json()["data"]["data"]['curGameId']
                    self.gamePublicKey = res.json()["data"]["data"]['extInfo']['pk']
            else:
                print(f"[{self.name}] ❌开始游戏失败,原因:",res.json()['ret'][0])
        except Exception as e:
            print(f"[{self.name}] ❎开始游戏失败")

    def settle_game(self,grantAmount):
        api = 'mtop.alsc.playgame.mini.game.play.settle'
        body = {
            "bizScene":"BLUE_KNIGHT_PARKOUR",
            "latitude": "30.17862595617771",
            "longitude": "120.22057268768549",
            "curGameId":self.curGameId,
            "actId":"20240204214413716190833090",
            "grantAmount":rsa_encrypt(self.gamePublicKey, str(grantAmount)),
            "propertyId":self.propertyId,
            "extParams":"{\"changeVersion\":\"20240412\"}"
            }
        data = json.dumps(body)
        try:
            res = self.xsign_req(api, data, "1.0")
            if res is None:
                return None
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                game_gold = res.json()["data"]["data"]["realGrantValue"]
                if game_gold:
                    print(f"[{self.name}] ✅游戏完成，获得--{game_gold}乐园币")
                else:
                    print(f"[{self.name}] ❌游戏完成，并没有获得奖励")
            else:
                if res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                    return None
                else:
                    print(f'[{self.name1}] ❎{res.json()["ret"][0]}')
                    return res.json()["ret"][0]
        except Exception:
            print(f'❎请求错误')
            return None

    def main(self):
        if self.login():
            self.query_game_info()
            print(f"----尝试领取游戏次数----")
            self.task()
            self.query_game_info()
            print(f"----尝试完成游戏----")
            if self.gameCount > 0:
                for i in range(self.gameCount):
                    self.start_game()
                    if self.curGameId:
                        print(f"模拟玩一次游戏中……")
                        settle_result = self.settle_game(25)
                        if settle_result and '发放数量超日限制' in settle_result:
                            break
            else:
                print(f"没有游戏次数可以玩了")


if __name__ == '__main__':
    if 'elmck' in os.environ:
        cookie = os.environ.get('elmck')
    else:
        print("环境变量中不存在[elmck],启用本地变量模式")
        cookie = ck
    if cookie == "":
        print("本地变量为空，请设置其中一个变量后再运行")
        exit(-1)
    cookies = cookie.split("&")
    print(f"饿了么共获取到 {len(cookies)} 个账号")
    for i, ck in enumerate(cookies):
        print(f"======开始第{i + 1}个账号======")
        TYT(ck).main()
        print("2s后进行下一个账号")
        time.sleep(2)
