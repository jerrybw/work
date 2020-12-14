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


def change(cno,enterprise_id,token,region,skill_id,password,name):
    create_exten_url = "https://api-"+region+".cticloud.cn/interface/v10/exten/create"
    create_agent_url = "https://api-"+region+".cticloud.cn/interface/v10/agent/create"
    change_bind_tel_url = "https://api-"+region+".cticloud.cn/interface/v10/agent/changeBindTel"
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'timestamp': timestamp,
        'sign': sign_md5,
        'cno': str(cno),
        'bindTel': str(cno),
        'bindType': 2,
        'isVerify': 0,
        "allow":"g729,alaw,ulaw",
        'areaCode': "010",
        'skillLevels': '1',
        "type":"3",
        "skillIds":skill_id,
        "name":name,
        "exten":str(cno),
        "password":password,
        "isDirect":"0"
    }
    create_agent_r = requests.post(create_agent_url, params)
    print(create_agent_r.json())
    create_exten_r = requests.post(create_exten_url, params)
    print(create_exten_r.json())
    bind_tel_r = requests.post(change_bind_tel_url, params)
    print(bind_tel_r.json())


if __name__ == "__main__":
    i = 4815
    flag1 = 45
    loop1 = 0
    while loop1 < flag1:
        loop1 += 1
        i += 1
        # change(i,"7600040","","6","1163","000000","360金融")

    j = 9265
    flag2 = 100
    loop2 = 0
    while loop2 < flag2:
        loop2 += 1
        j += 1
        change(j,"7600040","10f7e897ecfa03f731106e8b81abbb09","6","1163","000000","360金融")

    for cno in [10041,10042,10043,10044]:
        # change(cno,"7500066","","5","627","7500066",str(cno))
        pass
