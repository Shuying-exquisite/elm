import json
import os
import random
import time
import requests
from urllib.parse import quote
from datetime import datetime, date

nczlck = os.environ.get('elmck')

ck = ''

def tq(txt):
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


class LYB:
    def __init__(self, cki):
        self.name = None
        self.cki = tq(cki)
        self.uid = self.cki.get("unb")
        self.sid = self.cki.get("cookie2")
        self.token = self.cki.get("token")
        self.deviceId = self.cki.get("deviceId")
        self.host = 'https://acs.m.goofish.com'
        self.name1 = self.uid

    def xsign(self, api, data, wua, v):
        url = "接口"
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

        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                r = requests.post(url, json=body)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError as e:
                print(f'❎请求签名服务器失败: {e}')
            except requests.exceptions.Timeout:
                print("❎签名接口请求超时")
            except requests.exceptions.RequestException as e:
                print(f'❎请求签名服务器错误: {e}')
            retries += 1
            print(f"❎重试次数: {retries}")
            if retries >= max_retries:
                print("❎重试次数上限,尝试使用备用通道1")
                return self.xsign1(api, data, wua, v)

    def xsign1(self, api, data, wua, v):
        url = "http://114.55.90.197:5488/api/getXSign"
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

        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                r = requests.post(url, json=body, timeout=9)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError as e:
                print(f'❎请求签名服务器失败: {e}')
            except requests.exceptions.Timeout:
                print("❎签名接口请求超时")
            except requests.exceptions.RequestException as e:
                print(f'❎请求签名服务器错误: {e}')
            retries += 1
            print(f"❎重试次数: {retries}")
            if retries >= max_retries:
                print("❎通道1尝试次数上限,尝试使用备用通道2")
                return self.xsign2(api, data, wua, v)

    def xsign2(self, api, data, wua, v):
        url = "http://3.xjyyds.cf:18848/api/getXSign"
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

        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                r = requests.post(url, json=body, timeout=9)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError as e:
                print(f'❎请求签名服务器失败: {e}')
            except requests.exceptions.Timeout:
                print("❎签名接口请求超时")
            except requests.exceptions.RequestException as e:
                print(f'❎请求签名服务器错误: {e}')
            retries += 1
            print(f"❎重试次数: {retries}")
            if retries >= max_retries:
                print("❎通道2尝试次数上限,哦豁，签名通道都不可用！")
                return None

    def req(self, api, data, wua='False', v="1.0"):
        try:
            if type(data) == dict:
                data = json.dumps(data)
            wua = str(wua)
            sign = self.xsign(api, data, wua, v)
            url = f"{self.host}/gw/{api}/{v}/"
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

    def login(self):
        api1 = 'mtop.alsc.user.detail.query'
        try:
            res1 = self.req(api1, json.dumps({}), 'False', "1.0")
            if res1.json()['ret'][0] == 'SUCCESS::调用成功':
                self.name = res1.json()["data"]["encryptMobile"]
                api = 'mtop.koubei.interaction.center.common.queryintegralproperty.v2'
                data = json.dumps({"templateIds": "[\"1404\"]"})
                try:
                    res = self.req(api, data, 'False', "1.0")
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

    def yqm(self):
        api = 'mtop.ele.biz.growth.task.core.querytask'
        data = json.dumps({"bizScene": "ORCHARD", "missionCollectionId": "178", "accountPlan": "HAVANA_COMMON",
                           "locationInfos": "[\"{\\\"lng\\\":\\\"105.7647817209363\\\",\\\"lat\\\":\\\"30.59868285432458\\\"}\"]"})

        try:
            res = self.req(api, data, 'False', "1.0")
            if res is None:
                return None, None
            if res.json()["ret"][0] == "SUCCESS::接口调用成功":
                for y in res.json()['data']['mlist']:
                    if y['name'] == "果园日常人传人裂变任务-百川发奖":
                        actId = y['actionConfig']['ext']['actId']
                        shareId = y['actionConfig']['ext']['shareId']
                        return actId, shareId
            else:
                if res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print("❎cookie已过期，请重新获取")
                    return None, None
                else:
                    print(res.text)
                    return None, None
        except Exception:
            print(f'❎请求错误')
            return None, None

    def share(self, actid1, shareId1):
        api = 'mtop.alsc.play.component.snsshare.trigger.risk'
        data = json.dumps({"bizScene": "KB_ORCHARD", "shareId": shareId1, "actId": actid1, "requestId": "1720170483152",
                           "longitude": "99.75325090438128", "latitude": "99.597472842782736"})
        try:
            res = self.req(api, data, 'False', "1.0")
            if res is None:
                return None
            if res.json()["ret"][0] == "SUCCESS::接口调用成功":
                print(f"[{self.name1}] ✅助力成功")
                return True
            else:
                if res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                    return False
                else:
                    if res.json()["ret"][0] == "助力次数已用完":
                        print(f"[{self.name1}] ❎助力次数已用完")
                        return False
                    if res.json()["ret"][0] == "今日助力次数已用完":
                        print(f"[{self.name1}] ❎哦豁，莫得次数咯")
                        return False
                    if res.json()["ret"][0] == "SNS_RELATION_SELF:: 人传人关系是本人":
                        print(f"[{self.name1}] ❎不可给自己助力")
                        return False
                    if res.json()["ret"][0] == "SNS_RELATION_LIMIT_ERROR:: 人传人关系已达上限":
                        print(f"[{self.name1}] ❎助力上限\n")
                        return 'SX'
                    if res.json()["ret"][0] == " 人传人关系已达上限":
                        print(f"[{self.name1}] ❎助力上限\n")
                        return 'SX'
                    if res.json()["ret"][0] == "分享者已被助力成功，客态重复助力":
                        print(f"[{self.name1}] ❎重复助力")
                        return None
                    else:
                        print(f"[{self.name1}] ❎助力失败")
                        print(res.text)
                        return None
        except Exception as e:
            print(f'请求错误', e)
            return None

    def prize(self):
        global res, res1
        api1 = 'mtop.alsc.playgame.orchard.index.batch.query'
        data1 = json.dumps({
            "blockRequestList": "[{\"blockCode\":\"603040_6723057310\",\"status\":\"PUBLISH\",\"tagCallWay\":\"SYNC\",\"useRequestBlockTags\":false}]",
            "source": "KB_ORCHARD", "bizCode": "main",
            "locationInfos": "[{\"latitude\":\"99.597472842782736\",\"longitude\":\"99.75325090438128\",\"lat\":\"99.597472842782736\",\"lng\":\"99.75325090438128\"}]",
            "extData": "{\"ORCHARD_ELE_MARK\":\"KB_ORCHARD\",\"orchardVersion\":\"20240624\"}"})
        try:
            res1 = self.req(api1, data1, 'False', "1.0")
            if res1.json()["ret"][0] == "SUCCESS::调用成功":
                for y in res1.json()['data']['data']['603040_6723057310']['blockData']['instanceAssets']['tagData']:
                    for o in y['result']:
                        if o['name'] == "50g待领取水滴":
                            api2 = 'mtop.alsc.play.component.property.cert.trigger'
                            data2 = json.dumps(
                                {"actId": "20200629151859103125248022", "propertyId": o['instanceId'],
                                 "templateId": "561", "bizScene": "KB_ORCHARD"})
                            try:
                                res = self.req(api2, data2, 'False', "1.0")
                                if res.json()["ret"][0] == "SUCCESS::接口调用成功":
                                    amount1 = res.json()['data']['exchangeAmount']
                                    print(f"[{self.name}] ✅领取成功, 获得水滴--[{amount1}]g")
                                else:
                                    print(f"[{self.name}] ❎领取奖励失败:{res.text}")
                            except Exception as e:
                                print(res.text)
                                print(f'[{self.name}] 请求错误{e}')
                                return None
            else:
                if res1.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                else:
                    print(f"[{self.name}] ❎获取列表失败:", res1.json())
        except Exception as e:
            print(f"[{self.name}] 请求错误{e}")
            return None

    def signinfo(self):
        api = 'mtop.koubei.interactioncenter.orchard.sign.querysigninfo'
        data = json.dumps(
            {"latitude": "99.597472842782736", "longitude": "99.75325090438128", "bizScene": "orchard_signin"})
        try:
            res = self.req(api, data, 'False', "1.0")
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                date_time = datetime.now().strftime("%Y%m%d")
                for entry in res.json().get("data", {}).get("data", {}).get("signInPrizeList", []):
                    if entry["date"] == date_time:
                        for award in entry.get("ext", {}).get("awardInfo", []):
                            if award.get("status") != 'HAS_RECIVE':
                                prizeNumId = award.get("prizeNumId")
                                self.sign(prizeNumId, date_time)
        except Exception as e:
            print(f"[{self.name}] ❎请求错误{e}")
            return None

    def sign(self, prizeNumId, date_time):
        api = 'mtop.koubei.interactioncenter.orchard.sign.receivesigninaward'
        data = json.dumps({"latitude": "99.597472842782736", "longitude": "99.75325090438128", "signInDate": date_time,
                           "bizScene": "orchard_signin", "extInfo": "{\"prizeNumId\":\"" + prizeNumId + "\"}"})
        print(f"[{self.name}] ✅签到请求:{data}")
        try:
            res = self.req(api, data, 'False', "1.0")
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                print(f"[{self.name}] ✅签到成功")
            else:
                if res.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                    print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                else:
                    print(f"[{self.name}] ❎签到失败:{res.text}")
        except Exception as e:
            print(f"[{self.name}] ❎签到失败{e}")
            return None

    def warte(self):
        y, roleId, templateId, templateId1 = None, None, None, None
        amount, dygk, xygk, Sunlightvalue, remainingProgress = 0, 0, 0, 0, 0
        api = 'mtop.alsc.playgame.orchard.index.batch.query'
        data1 = json.dumps({
            "blockRequestList": "[{\"blockCode\":\"603040_6723057310\",\"status\":\"PUBLISH\",\"tagCallWay\":\"SYNC\",\"useRequestBlockTags\":false}]",
            "source": "KB_ORCHARD", "bizCode": "main",
            "locationInfos": "[{\"latitude\":\"99.597472842782736\",\"longitude\":\"99.75325090438128\",\"lat\":\"99.597472842782736\",\"lng\":\"99.75325090438128\"}]",
            "extData": "{\"ORCHARD_ELE_MARK\":\"KB_ORCHARD\",\"orchardVersion\":\"20240624\"}"})
        res3 = self.req(api, data1, 'False', "1.0")
        if res3.json()["ret"][0] == "SUCCESS::调用成功":
            for y in res3.json()['data']['data']['603040_6723057310']['blockData']['assets']['tagData']:
                for o in y['totalProps']:
                    if o['name'] == "水":
                        y = o['value']
                        amount = int(int(o['value']) / 10)
                    if o['name'] == "大阳光卡":
                        dygk = o['value']
                        templateId = o['templateId']
                    if o['name'] == "小阳光卡":
                        xygk = o['value']
                        templateId1 = o['templateId']
                    # if o['name'] == "3天浇水翻倍卡":
            for tag_data in res3.json()["data"]['data']["603040_6723057310"]["blockData"]["role"]["tagData"]:
                for result_data in tag_data["result"]:
                    for role_info in result_data["roleInfoDtoList"]:
                        if "roleBaseInfoDto" in role_info:
                            role_base_info = role_info["roleBaseInfoDto"]
                            if "roleId" in role_base_info:
                                roleId = role_base_info["roleId"]
            for tag_data in res3.json()["data"]["data"]["603040_6723057310"]["blockData"]["role"]["tagData"]:
                for result in tag_data["result"]:
                    for role_info in result["roleInfoDtoList"]:
                        for cc in role_info["rolePropertyInfoDtoList"]:
                            Sunlightvalue = cc["totalPropertyCnt"]
                            remainingProgress = role_info['roleLevelExpInfoDto']["remainingProgress"]
                            levelName = role_info['roleLevelExpInfoDto']["levelName"]
                            print(
                                f"✅水滴:{y}g\n✅可浇水：{amount}次\n✅阳光值: {Sunlightvalue}\n✅大阳光卡数量: {dygk}\n✅小阳光卡数量: {xygk}\n✅再浇水: {remainingProgress}%可{levelName}")
                            if int(Sunlightvalue) != 100:
                                if int(dygk) >= 1 and int(Sunlightvalue) <= 70:
                                    print(f"[{self.name}] ✅使用大阳光卡")
                                    for i in range(int(dygk)):
                                        api = 'mtop.alsc.playgame.orchard.roleoperate.useprop'
                                        data = json.dumps({"roleId": roleId, "roleType": "KB_ORCHARD",
                                                           "propertyTemplateId": templateId, "bizScene": "KB_ORCHARD",
                                                           "extParams": "{\"orchardVersion\":\"20240624\",\"popWindowVersion\":\"V2\"}"})
                                        res = self.req(api, data, 'False', "1.0")
                                        if res.json()["ret"][0] == "SUCCESS::调用成功":
                                            ygz = \
                                                res.json()['data']['data']['roleInfoDTO']['rolePropertyInfoDtoList'][0][
                                                    "totalPropertyCnt"]
                                            print(f"[{self.name}] ✅第[{i + 1}]次使用大阳光卡成功，当前阳光值:{ygz}")
                                            if 90 > int(ygz) > 80:
                                                print(f"[{self.name}] ✅阳光值达到80-90，停止使用大阳光卡")
                                                break
                                        elif res.json()["ret"][0] == "FAIL_BIZ_ROLE_USING_PROP_ENOUGH::已经是满状态":
                                            print(f"[{self.name}] ✅阳光值达到100，停止使用阳光卡")
                                            break
                                        else:
                                            print(f"[{self.name}] ❎第[{i + 1}]次使用大阳光卡失败:{res.text}")
                                elif int(xygk) >= 1:
                                    print(f"[{self.name}] ✅使用小阳光卡")
                                    for i in range(int(xygk)):
                                        api = 'mtop.alsc.playgame.orchard.roleoperate.useprop'
                                        data = json.dumps({"roleId": roleId, "roleType": "KB_ORCHARD",
                                                           "propertyTemplateId": templateId1, "bizScene": "KB_ORCHARD",
                                                           "extParams": "{\"orchardVersion\":\"20240624\",\"popWindowVersion\":\"V2\"}"})
                                        res = self.req(api, data, 'False', "1.0")
                                        if res.json()["ret"][0] == "SUCCESS::调用成功":
                                            print(f"[{self.name}] ✅第[{i + 1}]次使用小阳光卡成功")

                                        elif res.json()["ret"][0] == "FAIL_BIZ_ROLE_USING_PROP_ENOUGH::已经是满状态":
                                            print(f"[{self.name}] ✅阳光值达到100，停止使用阳光卡")
                                            break
                                        else:
                                            print(f"[{self.name}] ❎第[{i + 1}]次使用小阳光卡失败:{res.text}")
                                else:
                                    print(f"[{self.name}] ❎没有阳光卡可以用咯")
        else:
            if res3.json()["ret"][0] == "FAIL_SYS_SESSION_EXPIRED::Session过期":
                print(f"[{self.name1}] ❎cookie已过期，请重新获取")
                return 0, '0', 0
            else:
                print(f"[{self.name}] ❎获取列表失败:", res3.json())
                return 0, '0', 0
        return amount, roleId, Sunlightvalue

    def water(self):
        total_progress = 0
        total_watering = 0
        amount1, roleId1, Sunlightvalue = self.warte()
        if roleId1 == '0':
            return None
        
        for i1 in range(amount1):
            api = 'mtop.alsc.playgame.orchard.roleoperate.useprop'
            data2 = json.dumps({
                "propertyTemplateId": "462",
                "roleId": roleId1,
                "latitude": "99.597472842782736",
                "longitude": "99.75325090438128",
                "roleType": "KB_ORCHARD",
                "actId": "20200629151859103125248022",
                "collectionId": "20210812150109893985929183",
                "bizScene": "KB_ORCHARD",
                "extParams": "{\"orchardVersion\":\"20240624\",\"popWindowVersion\":\"V2\"}"
            })

            res2 = self.req(api, data2, 'False', "1.0")
            rede = res2.json()
            if rede["ret"][0] == "SUCCESS::调用成功":
                total_watering += 1
                if 'progress' in rede['data']['data']['extInfo']:
                    progress1 = float(rede['data']['data']['extInfo']['progress'])
                    if 'progressBySun' in rede['data']['data']['extInfo']:
                        progress = progress1 + float(rede['data']['data']['extInfo']['progressBySun'])
                    else:
                        progress = progress1
                    total_progress += progress
                    ygz = rede['data']['data']['roleInfoDTO']['rolePropertyInfoDtoList'][0]['totalPropertyCnt']
                    print(f"[{self.name}] ✅第{total_watering}次浇水成功,获得进度--[{progress}]")
                    if float(progress) < 0.02:
                        print(f"[{self.name}] ✅进度小于0.04，停止浇水")
                        break
                    if 'processRewardShow' in rede['data']['data']['roleInfoDTO']['processRewardDTO'] and 'openFlag' in \
                            rede['data']['data']['roleInfoDTO']['processRewardDTO']['processRewardShow']:
                        if rede['data']['data']['roleInfoDTO']['processRewardDTO']['processRewardShow']['openFlag']:
                            rewardId = rede['data']['data']['roleInfoDTO']['processRewardDTO']['processRewardShow'][
                                'rewardId']
                            self.warte11(roleId1, rewardId)
                else:
                    progress = 1
                    jg = rede['data']['data']['roleInfoDTO']['roleLevelExpInfoDto']['upgradeNeedValue']
                    zt = rede['data']['data']['roleInfoDTO']['roleLevelExpInfoDto']['levelName']
                    total_progress += progress
                    print(f"[{self.name}] ✅第{total_watering}次浇水成功,再浇水[{jg}]次可[{zt}]")
                    if 'processRewardShow' in rede['data']['data']['roleInfoDTO']['processRewardDTO'] and 'openFlag' in \
                            rede['data']['data']['roleInfoDTO']['processRewardDTO']['processRewardShow']:
                        if rede['data']['data']['roleInfoDTO']['processRewardDTO']['processRewardShow']['openFlag']:
                            rewardId = rede['data']['data']['roleInfoDTO']['processRewardDTO']['processRewardShow'][
                                'rewardId']
                            self.warte11(roleId1, rewardId)
            elif rede["ret"][0] == "FAIL_BIZ_ROLE_USING_PROP_EXP_ENOUGH::道具使用达到上限,明天再来吧":
                print(f"[{self.name}] ❎第{total_watering + 1}次浇水失败: 浇水上限")
                break
            else:
                if rede["ret"][0] == "FAIL_BIZ_ILLEGAL_ARGUMENT::角色id不能为空":
                    print(f"[{self.name}] ❎第{total_watering + 1}次浇水失败: 没种树浇个鸡毛水")
                    break
                else:
                    print(f"[{self.name}] ❎第{total_watering + 1}次浇水失败: {rede['ret'][0]}")
            time.sleep(random.randint(1, 3))
        print(f"浇水{total_watering}次获得进度: {total_progress}")

    def warte11(self, roleId1, rewardId):
        api = 'mtop.koubei.interactioncenter.orchard.processreward.receive'
        data = json.dumps(
            {"roleId": roleId1, "rewardId": rewardId, "longitude": "99.75325090438128",
             "latitude": "99.597472842782736", "bizScene": "KB_ORCHARD", "requestId": "1721029520763"})
        res = self.req(api, data, 'False', "1.0")
        if res.json()["ret"][0] == "SUCCESS::调用成功":
            if "rightSendDTOS" in res.json()['data']["data"]["lotteryResultDTO"]:
                for item in res.json()['data']["data"]["lotteryResultDTO"]["rightSendDTOS"]:
                    if "materialInfo" in item and "title" in item["materialInfo"]:
                        title = item["materialInfo"]["title"]
                        print(f"[{self.name}] ✅领取浇水奖成功,获得--[{title}]")
        else:
            print(f"[{self.name}] ❎领取浇水奖励失败:{res.text}")

    def pk(self):
        def task():
            api = 'mtop.ele.biz.growth.task.core.querytask'
            data2 = json.dumps({"bizScene": "ORCHARD", "missionCollectionId": "178", "accountPlan": "HAVANA_COMMON",
                               "locationInfos": "[\"{\\\"lng\\\":\\\"99.754552\\\",\\\"lat\\\":\\\"99.600419\\\"}\"]"})
            try:
                res3 = self.req(api, data2, 'False', "1.0")
                for tag_data in res3.json()["data"]["mlist"]:
                    for y in tag_data["missionStageDTOS"]:
                        if y["rewardStatus"] == "TODO":
                            skip_keywords = ['去提款', '神奇', '中国移动', '蚂蚁', '实付', '参与夺宝', '点淘', '快手',
                                             '支付宝', '公益林', '闲鱼', '淘特', '淘宝', '点击3个', '京东', 'UC极速版',
                                             '飞猪', '天猫', '喜马拉雅', '订阅', '完成实名认证', '完成指定动作奖励阳光卡', '每日餐点领水滴']
                            skip_task = False
                            for keyword in skip_keywords:
                                if keyword in tag_data["showTitle"]:
                                    skip_task = True
                                    break
                            if skip_task:
                                continue
                            name2 = tag_data["showTitle"]
                            missionDefId1 = tag_data["missionDefId"]
                            if tag_data["showTitle"] == "逛饿了么用户专属淘宝优惠":
                                count = '3'
                            elif tag_data["showTitle"] == "浏览外卖品质好店":
                                count = '2'
                            elif '邀请好友助力' in tag_data["showTitle"]:
                                count = '6'
                            else:
                                count = '1'
                            pageSpm = tag_data["actionConfig"]["actionValue"].get("pageSpm", "")
                            pageStageTime = tag_data["actionConfig"]["actionValue"].get("pageStageTime", "")
                            api = 'mtop.ele.biz.growth.task.event.pageview'
                            payload = {
                                "bizScene": "ORCHARD",
                                "accountPlan": "HAVANA_COMMON",
                                "collectionId": "178",
                                "missionId": missionDefId1,
                                "actionCode": "PAGEVIEW",
                                "asac": "2A20B11WIAXCI9QYYXRIR0",
                                "sync": "false"
                            }
                            if pageSpm:
                                payload['pageFrom'] = pageSpm
                            if pageStageTime:
                                payload['viewTime'] = pageStageTime
                            data2 = json.dumps(payload)
                            res3 = self.req(api, data2, 'False', "1.0")
                            if res3.json()["ret"][0] == "SUCCESS::接口调用成功":
                                print(f"[{self.name}] ✅[{name2}]任务完成")
                                which(name2, missionDefId1, count)
                            else:
                                print(f"[{self.name}] ❎完成任务失败: {res3.json()['ret'][0]}")
            except Exception as e:
                print(f"发生错误: {e}")

        def task1():
            global missionDefId, name
            api = 'mtop.ele.biz.growth.task.core.querytask'
            data2 = json.dumps({"bizScene": "ORCHARD", "missionCollectionId": "178", "accountPlan": "HAVANA_COMMON",
                               "locationInfos": "[\"{\\\"lng\\\":\\\"99.754552\\\",\\\"lat\\\":\\\"99.600419\\\"}\"]"})
            try:
                res = self.req(api, data2, 'False', "1.0")
                for tag_data in res.json()["data"]["mlist"]:
                    if tag_data["showTitle"] == "每日餐点领水滴":
                        for y in tag_data["missionStageDTOS"]:
                            if y["rewardStatus"] == "TODO":
                                name = tag_data["showTitle"]
                                missionDefId = tag_data["missionDefId"]
                        runtime = datetime.now().hour
                        if 11 <= runtime < 13:
                            count = '1'
                            which(name, missionDefId, count)
                        elif 17 <= runtime < 19:
                            count = '2'
                            which(name, missionDefId, count)
                        elif 21 <= runtime < 23:
                            count = '3'
                            which(name, missionDefId, count)
            except Exception as e:
                print(f"发生错误: {e}")

        def which(name1, missionId, count):
            if name1 != '每日餐点领水滴' and count != '6':
                for i1 in range(1, int(count) + 1):
                    api = 'mtop.ele.biz.growth.task.core.receiveprize'
                    data1 = json.dumps({
                        "bizScene": "ORCHARD",
                        "accountPlan": "HAVANA_COMMON",
                        "missionCollectionId": "178",
                        "missionId": missionId,
                        "count": i1,
                        "locationInfos": "[\"{\\\"lng\\\":99.75325090438128,\\\"lat\\\":99.597472842782736}\"]"
                    })
                    res3 = self.req(api, data1, 'False', "1.0")
                    if res3.json()["ret"][0] == "SUCCESS::接口调用成功":
                        print(f"[{self.name}] ✅[{name1}]奖励领取成功")
                    else:
                        print(f"[{self.name}] ❎[{name1}]奖励领取失败: {res3.json()['ret'][0]}")
            elif '邀请好友助力' in name1 or name1 == '每日餐点领水滴':
                api = 'mtop.ele.biz.growth.task.core.receiveprize'
                data1 = json.dumps({
                    "bizScene": "ORCHARD",
                    "accountPlan": "HAVANA_COMMON",
                    "missionCollectionId": "178",
                    "missionId": missionId,
                    "count": count,
                    "locationInfos": "[\"{\\\"lng\\\":99.75325090438128,\\\"lat\\\":99.597472842782736}\"]"
                })
                res3 = self.req(api, data1, 'False', "1.0")
                if res3.json()["ret"][0] == "SUCCESS::接口调用成功":
                    print(f"[{self.name}] ✅[{name1}]奖励领取成功")
                else:
                    print(f"[{self.name}] ❎[{name1}]奖励领取失败: {res3.json()['ret'][0]}")

        task()
        task1()

    def kb(self):
        date_time = datetime.now().hour
        if 7 <= date_time <= 9:
            api = 'mtop.ele.playgame.orchard.futurewater.receive'
            data = json.dumps({"bizScene": "KB_ORCHARD"})
            res = self.req(api, data, 'False', "1.0")
            if res.json()["ret"][0] == "SUCCESS::调用成功":
                print(f"[{self.name}] ✅领取成功")
            else:
                print(f"[{self.name}] ❎领取失败: {res.json()['ret'][0]}")

    def main(self):
        try:
            if self.login():
                self.kb()
                # self.signinfo()
                self.prize()
                self.pk()
                self.water()
        except Exception as e:
            print(f"[{self.name1}] 请求错误{e}")


def get_ck_usid(ck1):
    try:
        key_value_pairs = ck1.split(";")
        for pair in key_value_pairs:
            key, value = pair.split("=")
            if key.lower() == "userid":
                return value
    except Exception:
        return 'y'


if __name__ == '__main__':
    today = date.today()
    today_str = today.strftime('%Y%m%d')
    filename = f'{today_str}nc.json'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
        print("今日助力json文件不存在，已创建")
    else:
        print("今日助力json文件已存在")

    with open(filename, 'r') as file:
        data = json.load(file)

    if 'elmck' in os.environ:
        cookie = os.environ.get('elmck')
    else:
        print("❎环境变量中不存在[elmck],启用本地变量模式")
        cookie = ck
    if cookie == "":
        print("❎本地变量为空，请设置其中一个变量后再运行")
        exit(-1)
    cookies = cookie.split("&")

    zlck_list = nczlck.split("&")
    print(f"获取到 {len(zlck_list)} 个被助力账号")

    dzl_num = 0
    for zlck in zlck_list:
        dzl_num += 1
        lyb = LYB(zlck)
        actid, shareId = lyb.yqm()
        if actid is None or shareId is None:
            print("❎获取助力id失败")
        else:
            print(f"======被助力账号{dzl_num}获取邀请码成功,开始助力======")
            for i, ck in enumerate(cookies):
                usid = get_ck_usid(ck)
                zlcs = data.get(f"{usid}", 0)
                if zlcs < 3:
                    print(f"======被助力账号{dzl_num}-开始第{i + 1}/{len(cookies)}个账号助力======")
                    a = LYB(ck).share(actid, shareId)
                    if a == 'SX':
                        break
                    elif a:
                        data[f"{usid}"] = zlcs + 1
                        with open(filename, 'w') as file:
                            json.dump(data, file, indent=4)
                        print("2s后进行下一个账号")
                        time.sleep(2)
                        continue
                    elif a is False:
                        data[f"{usid}"] = 3
                        with open(filename, 'w') as file:
                            json.dump(data, file, indent=4)
                        print("2s后进行下一个账号")
                        time.sleep(2)
                        continue
                    else:
                        print("2s后进行下一个账号")
                        time.sleep(2)
                        continue
                else:
                    continue
        print(f"======被助力账号{dzl_num}-领取奖励并浇水======")
        lyb.main()
        print(f"======被助力账号{dzl_num}-任务结束======\n\n")
