import hashlib
import os
import re
import time
import requests
from urllib.parse import urlencode, quote

host = 'https://acs.m.goofish.com'

ck = ''


import json
import random
import string


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
        txt = txt.replace("zhuli;", "")
        txt = txt.replace("chushi;", "")
        txt = txt.replace("zhuli", "")
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
        if self.name1 is None:
            raise ValueError("❎获取USERID失败，跳过该账号")

    def req(self, api, data, v="1.0"):
        try:
            ck3 = check_cookie(self.ck)
            headers = {
                "authority": "shopping.ele.me",
                "accept": "application/json",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded",
                "cookie": ck3,
                "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
            }
            timestamp = int(time.time() * 1000)
            data_str = json.dumps(data)
            token = tq(ck3)
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

    def main(self):
        try:
            if self.login():
                return self.task()
        except Exception as e:
            print(f'❎登录失败: {e}')
            return False

    def login(self):
        amount = 0
        api1 = 'mtop.alsc.user.detail.query'
        data1 = {}
        try:
            res1 = self.req(api1, data1, "1.0")
            if res1.json()['ret'][0] == 'SUCCESS::调用成功':
                self.name = res1.json()["data"]["encryptMobile"]
                api = 'mtop.alibaba.svip.langrisser.query'
                data = {
                    "lgrsRequestItems": "[{\"backup\":false,\"count\":1,\"data\":{\"needHead\":true,\"month\":\"\"},\"resId\":\"867018\"}]",
                    "latitude": 30.59858, "longitude": 105.756336}
                try:
                    res = self.req(api, data, "1.0")
                    if res.json()['ret'][0] == 'SUCCESS::调用成功':
                        uu = res.json()['data']['data']['867018']['data']
                        for yyy in uu:
                            if 'peaCount' in yyy:
                                amount = yyy['peaCount']
                            print(f'[{self.name}] ✅登录成功,吃货豆----[{amount}]')
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
        try:
            api = 'mtop.alibaba.svip.langrisser.query'
            data = {"callSource": "biz_card_main", "lgrsRequestItems": "[{\"resId\":\"224166\",\"data\":{}}]",
                    "extra": "{\"source\":\"mtop\"}", "longitude": "105.75325090438128",
                    "latitude": "30.597472842782736"}
            res = self.req(api, data, "1.0")
            if res.json()['ret'][0] == 'SUCCESS::调用成功':
                for yyyy in res.json()['data']['data']['224166']['data']:
                    if yyyy['rewardStatus'] == 'TODO':
                        api1 = 'mtop.alibaba.svip.langrisser.act'
                        data1 = {
                            "extra": "{\"missionDefId\":" + str(yyyy[
                                                                    'distinctId']) + ",\"missionCollectionId\":36,\"missionType\":\"SIMPLESIGNIN\",\"source\":\"mtop\",\"asac\":\"2A21119A45TTVAEXP40N7N\",\"missionXId\":\"" +
                                     yyyy['missionXId'] + "\"}",
                            "resId": "223166", "callSource": "biz_code_main", "source": "mtop",
                            "longitude": "105.75325090438128", "latitude": "30.597472842782736"}
                        res = self.req(api1, data1, "1.0")
                        res1 = res.json()
                        if 'extend' in res1['data'] and 'value' in res1['data']['extend'] and res1['ret'][
                            0] == 'SUCCESS::调用成功':
                            print(f"[{self.name}] [{yyyy['showTitle']}]✅领取成功,获得{res1['data']['extend']['value']}个吃货豆")
                        else:
                            if 'msgInfo' in res1['data']:
                                print(f"[{self.name}] [{yyyy['showTitle']}]❌领取失败,原因:{res1['data']['msgInfo']}")
                            else:
                                print(f'[{self.name}] [{yyyy["showTitle"]}]❌领取失败{res.text}')
                        if 'pageStageTime' in yyyy:
                            api2 = 'mtop.ele.biz.growth.task.event.pageview'
                            data2 = {"collectionId": "36", "missionId": yyyy['distinctId'], "actionCode": "PAGEVIEW",
                                     "pageFrom": yyyy['pageSpm'],
                                     "viewTime": "15", "bizScene": "svip", "accountPlan": "HAVANA_COMMON", "sync": "true"}
                            res2 = self.req(api2, data2, "1.1")
                            if res2.json()['ret'][0] == 'SUCCESS::调用成功':
                                print(f"[{self.name}] [{yyyy['showTitle']}]✅领取成功")
                            else:
                                print(f'[{self.name}] [{yyyy["showTitle"]}]❌领取失败,原因:{res2.json()["ret"][0]}')
        except Exception as e:
            print(f"[{self.name}] ❌领取失败: {e}")


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
        ck = reorder_ck(ck)
        print(f"======开始第{i + 1}个账号======")
        TYT(ck).main()
        print("2s后进行下一个账号")
        time.sleep(2)
