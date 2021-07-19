import requests
import time
import hashlib
import codecs
import datetime
import os


def get_sign(enterprise_id,token,timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id  + token + str(timestamp)
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def request(url, params):
    return requests.post(url, data=params)


if __name__ == "__main__":
    # host = "vnc.vlink.cn"
    host = "39.97.196.29"
    bind_url = "http://"+host+"/interface/v3/axb/bwListSetting"
    app_id = "5600906"
    token = "5c356687f3530cea"
    params = {
        'action': "add",
        'type': "CallerParty",
        'expires': 30,
        'appId': app_id
    }
    for phone in ["17674759948","01023456789"]:
        timestamp = int(time.time())
        params["timestamp"] = timestamp
        params["bklist"]= phone
        sign_md5 = get_sign(app_id, token, timestamp)
        params["sign"]=sign_md5
        bind_r = request(bind_url, params)
        print(str(bind_r.json()))