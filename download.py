import requests
import time
import hashlib
import codecs


def get_sign(enterprise_id,token,timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def download(url,file_name):
    res = requests.get(url)
    res.raise_for_status()
    file = open(file_name, 'wb')
    for chunk in res.iter_content(100000):
        file.write(chunk)
    file.close()


def get_url(unique_id):
    get_file_name_url="https://api-test-2.cticloud.cn/interface/v10/rasrEvent/query"
    get_url_url="https://home-test-2.cticloud.cn/v1/report/callRecordQs/getUrl"
    timestamp = int(time.time())
    sign_md5 = get_sign("7000007", "", timestamp)
    cookies={'SESSION':'00467ff3-b596-4177-89dd-b41172dad940'}
    params = {
        'validateType': 2,
        "enterpriseId": "7000007",
        'timestamp': timestamp,
        'sign': sign_md5,
        "uniqueId.csv":unique_id,
        "recordType":"rasr",
        "recordFormat":1,
        "tenancyId":"TCC1000007",
        "organizationId":"JG2000006",
        "departmentId":"BM3000010",
        "download":1
    }
    get_file_name_r = requests.post(get_file_name_url,params)
    for record in get_file_name_r.json()["data"]:
        record_file = record["recordFile"]
        params["fileName"]=record_file
        get_url_r = requests.post(get_url_url,params,cookies=cookies)
        download(get_url_r.json()["result"],"record/"+record_file+".wav")


if __name__ == "__main__":
    get_unique_id_url="https://api-1.cticloud.cn/interface/v10/cdr/ib/query"
    get_rasr_url="https://api-1.cticloud.cn/interface/v10/rasrEvent/query"
    get_url_url="https://api-1.cticloud.cn/interface/v10/record/getUrl"
    enterprise_id = "7100001"
    token = ""
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id,token, timestamp)
    param = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'timestamp': timestamp,
        'recordType': "record",
        'sign': sign_md5,
        'limit':100,
        'callType':1,
        'download':1,
        "start":"0"
    }
    unique_ids = codecs.open(r"zhongan/uniqueId.csv", 'r', 'utf-8')
    for unique_id in unique_ids:
        tmp = unique_id.replace("\r","").replace("\n","")
        param["uniqueId"] = tmp
        rasr_r = requests.post(get_unique_id_url,param)
        print(rasr_r.json())
        for data in rasr_r.json()["data"]:
            recordFileName = data["recordFile"][0]["file"]
            param["recordFile"] = recordFileName
            # mp3_r = requests.post(get_url_url,param)
            # mp3_url = mp3_r.json()["data"]
            # download(mp3_url,"yueyu/both/"+str(tmp)+".mp3")
            param["recordFormat"] = 1
            param["recordSide"] = 2
            agent_wav_r = requests.post(get_url_url,param)
            agent_wav_url = agent_wav_r.json()["data"]
            download(agent_wav_url,"zhongan/"+str(tmp)+"-agent.wav")
            # download(wav_url,"yueyu/rasr/"+str(tmp)+".wav")
            param["recordSide"] = 1
            customer_wav_r = requests.post(get_url_url,param)
            customer_wav_url = customer_wav_r.json()["data"]
            download(customer_wav_url,"zhongan/"+str(tmp)+"-caustomer.wav")
        time.sleep(1)
