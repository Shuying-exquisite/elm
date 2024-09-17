import os
import re
import time
import datetime
import requests
from urllib.parse import urlencode, quote
import hashlib
import json
import random
import string

host = 'https://acs.m.goofish.com'

ck = ''


def generate_random_string(length=50):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def reorder_ck(s: str) -> str:
    order = ["cookie2", "sgcookie", "unb", "USERID", "SID", "token", "utdid", "deviceId", "umt"]
    cookies = s.split(';')
    cookie_dict = {}
    for cookie in cookies:
        key_value = cookie.split('=', 1)
        if len(key_value) == 2:
            key, value = key_value
            cookie_dict[key.strip()] = value.strip()
    reordered_cookies = []
    for key in order:
        if key in cookie_dict:
            reordered_cookies.append(f"{key}={cookie_dict[key]}")
    return ';'.join(reordered_cookies) + ';'


def get_ck_usid(ck1):
    key_value_pairs = ck1.split(";")
    for pair in key_value_pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            if key == "USERID":
                return value
    return '账号'


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


class TCS:
    def __init__(self, cki):
        self.stop = False
        self.ck = cki
        self.players = []
        self.name = None
        self.openId = None
        self.gameId = None
        self.gameToken = None
        self.cki = self.tq(cki)
        self.uid = self.cki.get("unb")
        self.sid = self.cki.get("cookie2")
        self.name1 = get_ck_usid(cki)

    def tq(self, txt):
        try:
            txt = txt.replace(" ", "")
            pairs = txt.split(";")[:-1]
            ck_json = {}
            for i in pairs:
                ck_json[i.split("=")[0]] = i.split("=")[1]
            return ck_json
        except Exception as e:
            print(f'❎Cookie解析错误: {e}')
            return {}

    def req(self, api, data, v="1.0"):
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
            if r:
                return r
            else:
                return None
        except Exception as e:
            return None

    def login(self):
        api1 = 'mtop.alsc.user.detail.query'
        data1 = {}
        try:
            res1 = self.req(api1, data1, "1.0")
            if res1.json()['ret'][0] == 'SUCCESS::调用成功':
                self.name = res1.json()["data"]["encryptMobile"]
                api = 'mtop.koubei.interaction.center.common.queryintegralproperty.v2'
                data = {"templateIds": "[\"1404\"]"}
                try:
                    res = self.req(api, data, "1.0")
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

    def getOpenId(self):
        api1 = 'mtop.alsc.playgame.mini.game.dispatch'
        data1 = {
            "bizMethod": "/init/init",
            "bizScene": "GREEDY_SNAKE",
            "bizParam": "{}"
        }
        try:
            res1 = self.req(api1, data1, "1.0")
            if res1.json()['ret'][0] == 'SUCCESS::调用成功':
                # print('获取Openid',res1.json())
                openId = json.loads(res1.json()['data']['data']).get('openId')
                self.openId = openId
                return True
            else:
                print(f'[{self.name1}] ❌获取Openid失败，原因:{res1.text}')
                return False
        except Exception as e:
            print(f"[{self.name1}] ❌获取Openid失败，原因: {e}")
            return False

    def startgame(self):
        api = 'mtop.alsc.playgame.mini.game.dispatch'
        data = {
            "bizMethod": "/game/start",
            "bizScene": "GREEDY_SNAKE",
            "bizParam": "{}"
        }
        try:
            res = self.req(api, data, "1.0")
            if res is None:
                return None
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                # print('开始游戏',res.json())
                players = json.loads(res.json()['data']['data']).get('players')
                gameId = json.loads(res.json()['data']['data']).get('gameId')
                gameToken = json.loads(res.json()['data']['data']).get('gameToken')
                # print('游戏玩家',resJson)
                self.players = players
                self.gameId = gameId
                self.gameToken = gameToken
                return True
            else:
                if res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                    return None
                else:
                    print(f'[{self.name1}] ❎{res.json()["ret"][0]}')
                    return None
        except Exception:
            print(f'❎请求错误')
            return None

    def gameScore(self):
        score = []
        i = 0
        # num = random.randint(5, 10)
        num = 3
        while i < num:
            key = random.randint(1, 14)
            item = self.players[key]
            player = {
                "openId": item.get('playerId'),
                "score": random.randint(800, 100000)
            }
            score.append(player)
            i = i + 1

        return score

    def endgame(self, count, len):
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        signStr = f'{len}&{self.gameToken}&{timestamp}'
        md = hashlib.md5(signStr.encode())
        gameSign = md.hexdigest()
        api = 'mtop.alsc.playgame.mini.game.dispatch'

        gameScore = json.dumps(self.gameScore())

        bizParam = json.dumps({
            "gameId": self.gameId,
            "gameResult": len,
            "time": timestamp,
            "gameSign": gameSign,
            "gameScore": gameScore,
        })

        data = {
            "bizMethod": "/game/end",
            "bizParam": bizParam,
            "bizScene": "GREEDY_SNAKE"
        }

        try:
            res = self.req(api, data, "1.0")
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                nested_data = json.loads(res.json()["data"]["data"])
                value = nested_data["realGrantValue"]
                if value is None:
                    print(f'[{self.name}] ❌第[{count}]次玩贪吃蛇失败,奖励上限')
                    self.stop = True
                else:
                    print(f'[{self.name}] ✅第[{count}]次玩贪吃蛇成功,获得乐园币--[{value}]')
                    self.stop = False
            else:
                print(f'[{self.name}] ❌游戏结算错误，原因:{res.text}')
                self.stop = False
        except Exception:
            print(f'❎请求错误')
            self.stop = False

    def task(self):
        count = 1
        len = 19999
        while count < 7 and self.stop is False:
            len = len + 1
            try:
                if self.getOpenId():
                    if self.startgame():
                        self.endgame(count, len)
                    else:
                        print(f'[{self.name1}] ❌开始游戏失败')
            except Exception as e:
                print(f"[{self.name1}] ❌游戏失败,原因: {e}")
            time.sleep(random.randint(1, 3))
            count = count + 1

    def main(self):
        if self.login():
            print(f"----开始游戏----")
            self.task()


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
        ck = reorder_ck(ck)
        TCS(ck).main()
