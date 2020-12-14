import requests
import time
import hashlib
import codecs


def get_sign(enterprise_id, token, timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def download(url, file_name):
    res = requests.get(url)
    res.raise_for_status()
    file = open(file_name, 'wb')
    for chunk in res.iter_content(100000):
        file.write(chunk)
    file.close()


def change(exten, pwd):
    update_exten_url = "https://api-6.cticloud.cn/interface/v10/exten/update"
    timestamp = int(time.time())
    sign_md5 = get_sign("7600040", "10f7e897ecfa03f731106e8b81abbb09", timestamp)
    params = {
        'validateType': 2,
        "enterpriseId": "7600040",
        'timestamp': timestamp,
        'sign': sign_md5,
        'exten': exten,
        'password': pwd,
        'areaCode': '010',
        'type': '3',
        "isDirect":"0"
    }
    update_agent_r = requests.post(update_exten_url, params)
    print(update_agent_r.json())
    return str(update_agent_r.json())


def get_pwd(exten):
    update_exten_url = "https://api-6.cticloud.cn/interface/v10/exten/get"
    timestamp = int(time.time())
    sign_md5 = get_sign("7600040", "", timestamp)
    params = {
        'validateType': 2,
        "enterpriseId": "7600040",
        'timestamp': timestamp,
        'sign': sign_md5,
        'exten': exten
    }
    update_agent_r = requests.post(update_exten_url, params)
    print(update_agent_r.json())
    return update_agent_r.json()["data"]["password"]


if __name__ == "__main__":
    # extens = range(8388,8741)
    change_pwd_log = codecs.open(r"change_pwd.log", 'w+', 'utf-8')
    extens_list = codecs.open(r"exten/exten.csv", 'r+', 'utf-8')
    for exten in extens_list:
        # pwd = str(get_pwd(exten))
        exten_l = exten.split(",")
        r = change(exten_l[0], exten_l[1])
        change_pwd_log.write(str(exten)+r+"\n")
    change_pwd_log.close()
