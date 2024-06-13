'use strict';

const got = require('got');
require('dotenv').config();
const { readFile } = require('fs/promises');
const path = require('path');

const qlDir = '/ql';
const fs = require('fs');
let Fileexists = fs.existsSync('/ql/data/config/auth.json');
let authFile="";
if (Fileexists)
  authFile="/ql/data/config/auth.json"
else
  authFile="/ql/config/auth.json"
//const authFile = path.join(qlDir, 'config/auth.json');

const api = got.extend({
  prefixUrl: 'http://127.0.0.1:5600',
  retry: { limit: 0 },
});

async function getToken() {
  const authConfig = JSON.parse(await readFile(authFile));
  return authConfig.token;
}

module.exports.getEnvs = async (envName='elmck') => {
  const token = await getToken();
  const body = await api({
    url: 'api/envs',
    searchParams: {
      searchValue: envName,
      t: Date.now(),
    },
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
    },
  }).json();
  return body.data;
};

async function getEnvsByName(name){
  const token = await getToken();
  const body = await api({
    url: 'api/envs',
    searchParams: {
      searchValue: name,
      t: Date.now(),
    },
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
    },
  }).json();
  return body.data;
}

module.exports.getEnvsByName =  getEnvsByName

module.exports.getEnvsCount = async () => {
  const data = await this.getEnvs();
  return data.length;
};

module.exports.addEnv = async (cookie, remarks) => {
  const token = await getToken();
  const body = await api({
    method: 'post',
    url: 'api/envs',
    params: { t: Date.now() },
    json: [{
      name: 'elmck',
      value: cookie,
      remarks,
    }],
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
      'Content-Type': 'application/json;charset=UTF-8',
    },
  }).json();
  return body;
};

module.exports.updateEnv = async (cookie, eid, remarks,envName='elmck') => {
  const token = await getToken();
  const body = await api({
    method: 'put',
    url: 'api/envs',
    params: { t: Date.now() },
    json: {
      name: envName,
      value: cookie,
      _id: eid,
      remarks,
    },
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
      'Content-Type': 'application/json;charset=UTF-8',
    },
  }).json();
  return body;
};

module.exports.updateEnv11 = async (cookie, eid, remarks,envName='elmck') => {
  const token = await getToken();
  const body = await api({
    method: 'put',
    url: 'api/envs',
    params: { t: Date.now() },
    json: {
      name: envName,
      value: cookie,
      id: eid,
      remarks,
    },
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
      'Content-Type': 'application/json;charset=UTF-8',
    },
  }).json();
  return body;
};

module.exports.DisableCk = async (eid) => {
  const token = await getToken();
  const body = await api({
    method: 'put',
    url: 'api/envs/disable',
    params: { t: Date.now() },
    body: JSON.stringify([eid]),
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
      'Content-Type': 'application/json;charset=UTF-8',
    },
  }).json();
  return body;
};

module.exports.EnableCk = async (eid) => {
  const token = await getToken();
  const body = await api({
    method: 'put',
    url: 'api/envs/enable',
    params: { t: Date.now() },
    body: JSON.stringify([eid]),
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
      'Content-Type': 'application/json;charset=UTF-8',
    },
  }).json();
  return body;
};

module.exports.getstatus = async(eid) => {
  var envs = await getEnvsByName('elmck');
  var tempid = 0;
  for (let i = 0; i < envs.length; i++) {
    tempid = 0;
    if (envs[i]._id) {
      tempid = envs[i]._id;
    }
    if (envs[i].id) {
      tempid = envs[i].id;
    }
    if (tempid == eid) {
      return envs[i].status;
    }
  }
  return 99;
};

module.exports.getEnvById = async(eid) => {
  const envs = await this.getEnvs();
  var tempid = 0;
  for (let i = 0; i < envs.length; i++) {
    tempid = 0;
    if (envs[i]._id) {
      tempid = envs[i]._id;
    }
    if (envs[i].id) {
      tempid = envs[i].id;
    }
    if (tempid == eid) {
      return envs[i].value;
    }
  }
  return "";
};

module.exports.getEnvByUserId = async (userId) => {
  const envs = await this.getEnvs('elmqqck');

  for (let i = 0; i < envs.length; i++) {
    let ck = envs[i].value
    const user_id = ck.match(/USERID=([^; ]+)(?=;?)/) ? ck.match(/USERID=([^; ]+)(?=;?)/)[0] : '123';

    if (user_id.indexOf(userId)!==-1) {
      return envs[i]
    }
  }
  return "";
};

module.exports.delEnv = async (eid) => {
  const token = await getToken();
  const body = await api({
    method: 'delete',
    url: 'api/envs',
    params: { t: Date.now() },
    body: JSON.stringify([eid]),
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`,
      'Content-Type':'application/json;charset=UTF-8',
    },
  }).json();
  return body;
};
