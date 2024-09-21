/**
 * 饿了么 - 我要当总裁
*/

const $ = new Env('饿了么-我要当总裁');
const {
  cookiesToMap,
  elmRequestByApi,
  elmRequestByH5
} = require('./comm');


class Task {
  constructor(cookie, index) {
    this.cookie = cookie
    this.cookieObject = cookiesToMap(cookie)
    this.uid = this.cookieObject.get('USERID')
    this.index = index + 1

    this.count = 1
  }

  // 获取token
  async getToken(){
    const api = 'mtop.alsc.playgame.mini.game.dispatch'
    const data = JSON.stringify({
      "bizScene": "TOBECEO", 
      "bizMethod": "login", 
      "bizParam": "{\"gameId\":\"\"}",
      "longitude": "104.09800574183464", 
      "latitude": "30.22990694269538"
    })
    let res = await elmRequestByH5(this.cookie, api, data);
    if(res.ret.indexOf('SUCCESS::调用成功') > -1){
      let jsonData = JSON.parse(res.data.data)
      this.token = jsonData.data.token
      this.gameId = jsonData.data.token
      // console.log('获取游戏token，',this.token)
      // console.log('获取游戏gameId，',this.gameId)
      return true
    }
    console.log('['+this.uid+'] 获取 token/gameid 出错----',res.ret)
    return false
  }

  // 开始游戏
  async startGame(){
    const api = 'mtop.alsc.playgame.mini.game.dispatch'
    const data = JSON.stringify({
      "bizScene": "TOBECEO", "bizMethod": "startGame",
      "bizParam": "{\"gameId\":\"" + this.gameId + "\",\"token\":\"" + this.token + "\"}",
      "longitude": "104.09800574183464",
      "latitude": "30.22990694269538"
    })

    let res = await elmRequestByH5(this.cookie, api, data);
    if(res.ret.indexOf('SUCCESS::调用成功') > -1){
      let jsonData = JSON.parse(res.data.data)
      if(jsonData.bizErrorMsg == 'success'){
        this.gameCode = jsonData.data.gameMatch.gameCode
        console.log('['+this.uid+'] 开始游戏，游戏码----')
        return true
      }
      console.log('['+this.uid+'] 没有游戏次数了----',jsonData.bizErrorMsg)
      return false
    }
    console.log('['+this.uid+'] 开始游戏出错----',res.ret)
    return false
  }

  // 结束游戏
  async endGame(){
    const api = 'mtop.alsc.playgame.mini.game.dispatch'
    const data = JSON.stringify({
      "bizScene": "TOBECEO", 
      "bizMethod": "endGame",
      "bizParam": "{\"gameId\":\"" + this.gameId + "\",\"gameCode\":\"" + this.gameCode + "\",\"operationQueue\":[[4,6],[9,1],[6,4],[9,1],[1,9],[8,2],[5,5],[8,2],[2,8],[5,5],[1,9],[8,2],[5,5],[1,9],[8,2],[5,5],[8,2],[2,8],[5,5],[1,9],[8,2],[5,5],[8,2],[2,8],[5,5],[1,9],[8,2],[5,5],[8,2],[2,8],[5,5],[8,2],[2,8],[5,5],[5,5],[6,4],[3,7],[1,9],[9,1],[6,4],[3,7],[6,4],[1,9],[8,2],[5,5],[8,2],[2,8],[5,5],[1,9],[8,2],[5,5],[8,2],[2,8],[5,5],[6,4]],\"token\":\"" + this.token + "\"}",
      "longitude": "104.09800574183464", 
      "latitude": "30.22990694269538"
    })

    let res = await elmRequestByH5(this.cookie, api, data);
    if(res.ret.indexOf('SUCCESS::调用成功') > -1){
      console.log('['+this.uid+'] 结束游戏----')
      return true
    }
    console.log('['+this.uid+'] 结束游戏出错----',res.ret)
    return false
  }

  // 看广告
  async getPageview(){
    const api = "mtop.ele.biz.growth.task.event.pageview"
    const data = JSON.stringify({
        "collectionId": "1477", 
        "missionId": "25380001", 
        "actionCode": "PAGEVIEW", 
        "bizScene": "FOOD_ELIMINATE", 
        "accountPlan": "KB_ORCHARD", 
        "locationInfos": "[\"{\\\"lng\\\":\\\"-360\\\",\\\"lat\\\":\\\"-360\\\"}\"]"
    })

    let res = await elmRequestByApi(api, data, this.cookie);
    if(res.ret[0] =='SUCCESS::接口调用成功'){
      console.log('开始看广告----')
      return true
    }
    console.log('看广告出错----', res ? res.ret : 'res未定义');
    return false
  }

  // 领取道具
  async postPageview(){
    await $.wait(3000);
    const api = "mtop.ele.biz.growth.task.core.receiveprize"
    let extInfo = JSON.stringify({
      "count":9,
      "gameId":this.gameId,
      "type":"GameProp",
      "costType":"Ads",
      "itemId":"D001",
      "token":this.token
    })
    const data = JSON.stringify({
      "missionCollectionId":"1477",
      "missionId":"25380001",
      "count":this.count,
      "extInfo":extInfo,
      "missionXId":"",
      "instanceId":"",
      "umiToken":"1",
      "ua":"1",
      "locationInfos":"[\"{\\\"lng\\\":104.09800574183464,\\\"lat\\\":30.22990694269538,\\\"city\\\":\\\"511400\\\"}\"]",
      "longitude":"104.09800574183464",
      "latitude":"30.22990694269538"
    })

    let res = await elmRequestByApi(api, data, this.cookie);
    if(res.ret[0] =='SUCCESS::接口调用成功'){
      console.log('['+this.uid+'] 领取道具----')
      return true
    }
    console.log('['+this.uid+'] 领取道具出错----',res.ret)
    return false

  }

  // 使用道具
  async usedGameProp(){
    const api = 'mtop.alsc.playgame.mini.game.dispatch'
    const data = JSON.stringify({
      "bizScene":"TOBECEO",
      "bizMethod":"useGameProp",
      "bizParam": "{\"gameId\":\"" + this.gameId + "\",\"token\":\"" + this.token + "\"}",
      "longitude": "104.09800574183464",
      "latitude": "30.22990694269538"
    })

    let res = await elmRequestByH5(this.cookie, api, data);
    if(res.ret.indexOf('SUCCESS::调用成功') > -1){
      let jsonData = JSON.parse(res.data.data)
      if(jsonData.bizErrorMsg == 'success'){
        console.log('['+this.uid+'] 使用道具成功')
        this.count++
        return true
      }
      
      console.log('['+this.uid+'] 使用道具出错----',jsonData.bizErrorMsg)
      return false
    }
    console.log('['+this.uid+'] 使用道具出错----',res.ret)
    return false
  }

  // 获取任务列表
  async getTaskList(){
    const api = 'mtop.alsc.playgame.mini.game.dispatch'
    const data = JSON.stringify({
      "bizScene":"TOBECEO",
      "bizMethod":"getTasks",
      "bizParam": JSON.stringify({
        "gameId":this.gameId,
        "token":this.token
      }),
      "longitude": "104.09800574183464",
      "latitude": "30.22990694269538"
    })

    let res = await elmRequestByH5(this.cookie, api, data);
    if(res.ret.indexOf('SUCCESS::调用成功') > -1){
      let jsonData = JSON.parse(res.data.data)
      if(jsonData.bizErrorMsg == 'success'){
        this.taskList = jsonData.data.tasks
        if(Object.keys(this.taskList).length > 0){
          console.log('['+this.uid+'] 获取任务列表成功----')
          return true
        }
        console.log('['+this.uid+'] 还没有待领奖任务')
        return false
      }
      console.log('['+this.uid+'] 获取任务列表出错----',jsonData.bizErrorMsg)
      return false
    }
    console.log('['+this.uid+'] 获取任务列表出错----',res.ret)
    return false
  }

  // 校验任务是否完成
  async checkTask(){
    if(await this.getTaskList()){
      // 判断是否使用道具
      // if("T001" in this.taskList){
      //   if(this.taskList['T001']['isFinishe'] == true){
      //     console.log('✅任务T001已完成')
      //   }else if(this.taskList['T001']['progress'] == 4){
      //     console.log('领取T001奖励')
      //     this.postTask(this.taskList['T001']['taskId'])
      //   }else{
      //     console.log('T001任务进度',this.taskList['T001']['progress']+"/4")
      //     console.log('继续T001任务')
      //   }
      // }

      // 判断是否完成任务
      if("T004" in this.taskList){
        if(this.taskList['T004']['isFinishe'] == true){
          console.log('['+this.uid+'] ✅任务T004已完成')
          return false
        }else if(this.taskList['T004']['progress'] == 100){
          console.log('['+this.uid+'] 领取T004奖励')
          this.postTask(this.taskList['T004']['taskId'])
          return false
        }else{
          console.log('['+this.uid+'] T004任务进度',this.taskList['T004']['progress']+"/4")
          console.log('['+this.uid+'] 继续T004任务')
          return true
        }
      }
    }

    return true
    
  }

  // 领取任务奖励
  async postTask(taskId){
    const api = 'mtop.alsc.playgame.mini.game.dispatch'
    const data = JSON.stringify({
      "bizScene":"TOBECEO",
      "bizMethod":"finisheTask",
      "bizParam": JSON.stringify({
        "taskId":taskId,
        "gameId":this.gameId,
        "token":this.token
      }),
      "longitude": "104.09800574183464",
      "latitude": "30.22990694269538"
    })

    let res = await elmRequestByH5(this.cookie, api, data);
    if(res.ret.indexOf('SUCCESS::调用成功') > -1){
      let jsonData = JSON.parse(res.data.data)
      if(jsonData.bizErrorMsg == 'success'){
        console.log(`[${this.uid}] ✅完成任务获得乐园币--[${jsonData['data']['rewardItems'][0]['num']}]`)
      }else{
        console.log('['+this.uid+'] 完成任务'+taskId+'出错----',jsonData.bizErrorMsg)
      }
    }
  }

  async main() {
    // 获取 token
    console.log('*****第【' + this.uid + '】个账号【' + this.uid + '】开始 *****')
    if (await this.getToken())
      // 获取任务列表
      if (await this.checkTask()) {
        if (await this.startGame()) {
          await this.getPageview()
          await this.postPageview()
          await this.usedGameProp()
          await this.endGame()

          // 领取奖励  
          await this.getTaskList()
          if ("T004" in this.taskList) {
            if (this.taskList['T004']['isFinishe'] == true) {
              console.log('[' + this.uid + '] ✅任务T004已完成')
            } else if (this.taskList['T004']['progress'] == 100) {
              console.log('[' + this.uid + '] 领取T004奖励')
              await this.postTask(this.taskList['T004']['taskId'])
            } else {
              console.log('[' + this.uid + '] T004任务进度', this.taskList['T004']['progress'] + "/4")
              console.log('[' + this.uid + '] 继续T004任务')
            }
          }

          // 领取奖励  道具
          if ("T001" in this.taskList) {
            if (this.taskList['T001']['isFinishe'] == true) {
              console.log('✅任务T001已完成')
            } else if (this.taskList['T001']['progress'] == 4) {
              console.log('领取T001奖励')
              await this.postTask(this.taskList['T001']['taskId'])
            } else {
              console.log('T001任务进度', this.taskList['T001']['progress'] + "/4")
            }
          }

        }
      }
    console.log('*****第【' + this.uid + '】个账号【' + this.uid + '】结束 *****')
  }
}

async function start() {
  // 获取账号
  let cookies = []
  if (process.env.elmck) {
    // 环境变量
    if (process.env.elmck.indexOf('&') > -1) {
      cookies = process.env.elmck.split('&');
    } else {
      cookies.push(process.env.elmck);
    }
    console.log(`执行账号个数：${cookies.length}`);
  } else {
    // 本地测试
    cookies = cookies.concat([
      ''
    ])
    if (cookies.length < 1) {
      log("检测到环境变量、本地ck都为空");
      return;
    }
  }

  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i];
    const task = new Task(cookie, i);
    await task.main();
    $.log('等待3秒')
    await $.wait(3000)
  }

}

start()


// prettier-ignore
function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }

