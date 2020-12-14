import requests
import time
import hashlib
import codecs


def get_sign(enterprise_id,token,timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def request(url, params):
    return requests.post(url, data=params)


if __name__ == "__main__":
    agents = codecs.open(r"toutiaohr.csv", 'r', 'utf-8')
    create_agent_url="https://api-2.cticloud.cn/interface/v10/agent/create"
    update_agent_url="https://api-2.cticloud.cn/interface/v10/agent/update"
    create_exten_url="https://api-2.cticloud.cn/interface/v10/exten/create"
    bind_exten_url="https://api-2.cticloud.cn/interface/v10/agent/changeBindTel"
    enterpriseId = "7000437"
    token = ""
    params = {
        'validateType': 2,
        "enterpriseId": enterpriseId,
        'timestamp': 0,
        'sign': "",
        'agentType': 2,
        'obClidType': 2,
        'skillLevels':'1',
        'password':'8888',
        'type':3,
        'allow':'g729,alaw,ulaw',
        'bindType':2,
        'isVerify':0,
        'isDirect':1
    }
    for line in agents:
        agent = line.split(",")
        timestamp = int(time.time())
        sign_md5 = get_sign(enterpriseId, token, timestamp)
        params["timestamp"] = timestamp
        params["sign"]=sign_md5
        params["cno"] = agent[1]
        params["name"] = agent[1]
        params["areaCode"]=agent[0]
        params["obClid"]=agent[2]
        params["skillIds"]=agent[3]
        params["exten"]=agent[1]
        params["bindTel"]=agent[1]
        print(params)
        create_agent_r = request(create_agent_url,params)
        print(create_agent_r.json())
        create_exten_r = request(create_exten_url,params)
        print(create_exten_r.json())
        bind_exten_r = request(bind_exten_url,params)
        print(bind_exten_r.json())
        # for i in range(0,5):
        #     tmp = str(agent[1])
        #     if not i == 0:
        #         tmp = str(agent[1])+str(i)
        #     params["timestamp"] = timestamp
        #     params["sign"] = sign_md5
        #     params["cno"] = tmp
        #     params["name"] = tmp
        #     params["areaCode"] = agent[0]
        #     params["obClid"] = agent[2]
        #     params["skillIds"] = agent[3]
        #     params["exten"] = tmp
        #     params["bindTel"] = tmp
        #     print(params)
        #     create_agent_r = request(create_agent_url, params)
        #     print(create_agent_r.json())
        #     create_exten_r = request(create_exten_url, params)
        #     print(create_exten_r.json())
        #     bind_exten_r = request(bind_exten_url, params)
        #     print(bind_exten_r.json())
    agents.close()
