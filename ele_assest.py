import json
import os
import random
import datetime
import requests
from urllib.parse import quote

host = 'https://acs.m.goofish.com'
xsign_host = "接口"

class LYB:
    def __init__(self, cki):
        self.ck1 = self.tq(cki)
        self.ck = cki

    def tq(self, txt):
        try:
            txt = txt.replace(" ", "")
            pairs = txt.split(";")[:-1]
            ck_json = {i.split("=")[0]: i.split("=")[1] for i in pairs}
            return ck_json
        except Exception as e:
            print(f"", end="")
            return {}

    def xsign(self, api, data, uid, sid, wua, v):
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
                xsign_host,
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

    def req(self, api, data, uid, sid, wua='False', v="1.0"):
        try:
            if type(data) == dict:
                data = json.dumps(data)
            wua = str(wua)
            sign = self.xsign(api, data, uid, sid, wua, v)
            url = f"{host}/gw/{api}/{v}/"
            headers = {
                "x-sgext": quote(sign.get('x-sgext')),
                "x-sign": quote(sign.get('x-sign')),
                'x-sid': sid,
                'x-uid': uid,
                'x-sv': '3.3.0',
                'x-pv': '6.3',
                'x-features': '1051',
                'x-mini-wua': quote(sign.get('x-mini-wua')),
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'x-t': sign.get('x-t'),
                'x-umt': sign.get('x-umt'),
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

    def yqm(self):
        if 'ZL_CK' in os.environ:
            cki = self.tq(os.environ.get('ZL_CK'))
        else:
            cki = self.tq(self.ck)
        if not cki:
            print("❎被助力账号为空，请设置后再运行")
            return None, None
        uid = cki.get("unb")
        sid = cki.get("cookie2")

        api = 'mtop.ele.biz.growth.task.core.querytask'
        data = json.dumps({"missionCollectionId": "839",
                           "locationInfos": "[\"{\\\"lng\\\":\\\"105.75325090438128\\\",\\\"lat\\\":\\\"30.597472842782736\\\"}\"]",
                           "bizScene": "game_center", "accountPlan": "HAVANA_COMMON"})
        try:
            res = self.req(api, data, uid, sid, "1.0")
            if res is None:
                return None, None
            if res.json()["ret"][0] == "SUCCESS::接口调用成功":
                mlist = res.json()["data"]['mlist']
                for item in mlist:
                    if 'actionConfig' in item and 'ext' in item['actionConfig']:
                        actid = item['actionConfig']['ext']['actId']
                        shareId = item['actionConfig']['ext']['shareId']
                        return actid, shareId
            elif res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                print("❎ck过期", end=' ')
                return None, None
            else:
                print(res.text)
        except Exception as e:
            print(f'❎请求错误: {e}')
        print("❎获取助力id失败\n")
        return None, None

    def share(self, actid1, shareId1, usid):
        cki = self.ck1
        uid = cki.get("unb")
        sid = cki.get("cookie2")
        api = 'mtop.koubei.interactioncenter.share.common.triggershare'
        data = json.dumps(
            {"actId": actid1, "shareId": shareId1, "bizScene": "DEFAULT", "requestId": "1719848804784"})
        try:
            res = self.req(api, data, uid, sid, "1.0")
            if res is None:
                return None
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                print(f"✅助力成功\n")
                return True
            else:
                if res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    ck_updated = self.update_ck(cki)
                    if not ck_updated:
                        print(f"❎助力ck过期\n")
                        return False
                    else:
                        return self.share(actid1, shareId1, usid)
                else:
                    if res.json()["data"]['errorMsg'] == "助力次数已用完":
                        print(f"❎助力次数已用完", end="\n")
                        return False
                    if res.json()["data"]['errorMsg'] == "今日助力次数已用完":
                        print(f"❎莫得次数咯", end="\n")
                        return False
                    if res.json()["data"]['errorMsg'] == " 人传人关系已达上限":
                        print(f"❎助力上限", end="\n")
                        return 'SX'
                    if res.json()["data"]['errorMsg'] == "分享者已被助力成功，客态重复助力":
                        print(f"❎重复助力", end="\n")
                        return None
                    else:
                        print(f"❎助力失败", end="\n")
                        print(res.text)
                        return None
        except Exception as e:
            print(f'请求错误: {e}')
            return None

    def prize(self):
        if 'ZL_CK' in os.environ:
            cki = self.tq(os.environ.get('ZL_CK'))
        else:
            cki = self.tq(self.ck)
        if not cki:
            print("被助力账号为空，请设置后再运行")
            return
        uid = cki.get("unb")
        sid = cki.get("cookie2")
        api1 = 'mtop.ele.biz.growth.task.core.querytask'
        data1 = json.dumps({"missionCollectionId": "839",
                            "locationInfos": "[\"{\\\"lng\\\":\\\"105.75325090438128\\\",\\\"lat\\\":\\\"30.597472842782736\\\"}\"]",
                            "bizScene": "game_center", "accountPlan": "HAVANA_COMMON"})
        try:
            res1 = self.req(api1, data1, uid, sid, "1.0")
            if res1 is None:
                return
            if res1.json()["ret"][0] == "SUCCESS::接口调用成功":
                for y in res1.json()['data']['mlist']:
                    if y['name'] == "邀请好友助力":
                        for o in y['missionStageDTOS']:
                            if o['rewardStatus'] == "TODO" and o['status'] == "FINISH":
                                api = 'mtop.ele.biz.growth.task.core.receiveprize'
                                data2 = json.dumps({
                                    "missionCollectionId": "839",
                                    "missionId": "20544001",
                                    "count": o['stageCount']
                                })
                                try:
                                    res = self.req(api, data2, uid, sid, "1.0")
                                    if res is None:
                                        continue
                                    data = res.json()["data"]
                                    if data.get('errorMsg') is not None:
                                        print(f"❎领取奖励失败: {data['errorMsg']}\n")
                                    else:
                                        rlist = data.get('rlist')
                                        if rlist is not None:
                                            print(f"✅领取奖励成功--{rlist[0]['value']}乐园币", end="\n")
                                        else:
                                            print(f"❎{res.json()['ret'][0]}")
                                except Exception as e:
                                    print(f'请求错误: {e}')
                                    continue
            else:
                if res1.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print(f"")
                else:
                    print(f"❎获取列表失败:", res1.json()["data"]['errorMsg'])
        except Exception as e:
            print(f'请求错误: {e}')
            return

    def update_ck(self, cki):
        ck = self.ck
        update_url = "http://47.98.134.8:14499/elmxq"
        data = {'cookie': ck}
        response = requests.post(update_url, json=data)
        if response and response.status_code == 200:
            result = response.json()
            if result.get('message') == '刷新成功':
                expirationTime = result.get('expirationTime')
                print(f'cookie续期成功:{expirationTime}', end="\n")
                self.ck = result.get('cookie')
                self.ck1 = self.tq(self.ck)
                return True
            elif result.get('message') == '刷新失败':
                print(f'cookie续期失败')
        return False



def get_ck_usid(ck):
    ck1 = ck.replace("==","")
    key_value_pairs = ck1.split(";")
    for pair in key_value_pairs:
        if '=' not in pair:
            continue
        key, value = pair.split("=")
        if key == "USERID":
            return value
    return None


if __name__ == '__main__':
    today = datetime.date.today()
    today_str = today.strftime('%Y%m%d')
    filename = f'{today_str}.json'
    
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
        print("今日助力json文件不存在，已创建")
    else:
        print("今日助力json文件已存在")

    with open(filename, 'r') as file:
        data = json.load(file)


    ck = os.environ.get('elmck')
    ck_list = ck.split("&") if ck else []
    random.shuffle(ck_list)
    print(f"获取到 {len(ck_list)} 个随机打乱顺序的助力账号")

    zlck = os.environ.get('elmzlck')
    zlck_list = zlck.split("&") if zlck else []
    print(f"获取到 {len(zlck_list)} 个被助力账号")

    for dzl_num, zlck in enumerate(zlck_list, start=1):
        lyb = LYB(zlck)
        actid, shareId = lyb.yqm()
        if actid is None or shareId is None:
            print("❎获取助力id失败\n")
            continue
        print(f"🐂🍺>>>开始给第{dzl_num}/{len(ck_list)}个账号助力->获取邀请码成功->>")

        for i, ck in enumerate(ck_list):
            if len(ck) >200:
                usid = get_ck_usid(ck)
                zlcs = data.get(f"{usid}", 0)
                if zlcs < 3:
                    print(f">>>第{i + 1}个", end="")
                    try:
                        a = LYB(ck).share(actid, shareId, usid)
                        if a is None:
                            continue
                        elif a == 'SX':
                            
                            break
                        else:
                            data[f"{usid}"] = zlcs + 1
                            with open(filename, 'w') as file:
                                json.dump(data, file, indent=4)
                        
                    except Exception as e:
                        print(f"❎助力时发生错误: {e}")
                        continue
            else:
                print("网页CK，暂时跳过\n")
        print("\n======助力结束,领取奖励======")

        try:
            lyb.prize()
        except Exception as e:
            print(f"❎领取奖励时发生错误: {e}")
        print(f"======被助力账号{dzl_num}-助力结束======\n")

