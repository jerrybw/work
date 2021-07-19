import requests
import time
import hashlib
import codecs
import json


def get_sign(enterprise_id,token,timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def get_skill(cno,region,enterprise_id,token):
    get_skill_url = "https://api-" + region + ".cticloud.cn/interface/v10/agent/queryAgentSkill"
    timestamp = int(time.time())
    skill_str = ""
    skill_level_str = ""
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'timestamp': timestamp,
        'sign': get_sign(enterprise_id,token,timestamp),
        "cnos":cno
    }
    get_skill_r = requests.post(get_skill_url,params)
    if str(get_skill_r.json()["result"]) != "0":
        return False,str(get_skill_r.json()),skill_level_str
    if len(get_skill_r.json()["data"]) == 0:
        return False, str(get_skill_r.json()),skill_level_str
    for skill in get_skill_r.json()["data"]:
        skill_str = skill_str + str(skill["skillId"]+",")
        skill_level_str= skill_level_str + str(skill["skillLevel"]+",")
    return True,skill_str,skill_level_str



def change_agent_skill(cno,skill,skill_level,region,enterprise_id,token):
    change_agent_url = "https://api-" + region + ".cticloud.cn/interface/v10/agent/update"
    timestamp = int(time.time())
    skill_str = ""
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'timestamp': timestamp,
        'sign': get_sign(enterprise_id,token,timestamp),
        "cno":cno,
        "skillIds":skill,
        "skillLevels":skill_level
    }
    change_agent_r = requests.post(change_agent_url,params)
    return str(change_agent_r.json())


if __name__ == "__main__":
    change_agent_log = codecs.open(r"change_agent.log", 'w+', 'utf-8')
    data_resource = codecs.open(r"cno.csv", 'r', 'utf-8')
    skill_data_resource = codecs.open(r"skill.csv", 'r', 'utf-8')
    skill_map = {}
    for skill_data in skill_data_resource:
        skill_data_str_list = skill_data.replace("\r", "").replace("\n", "").split(",")
        print(skill_data_str_list[0], skill_data_str_list[1])
        skill_map[skill_data_str_list[0]] = skill_data_str_list[1]
    for data in data_resource:
        data_str_list = data.replace("\r", "").replace("\n", "").split(",")
        print(data_str_list[0],data_str_list[1],skill_map[data_str_list[1]])
        cno = data_str_list[0]
        skill = skill_map[data_str_list[1]]
        flag,skill_str_tmp,skill_level_str_tmp = get_skill(cno,"2","7000005","3dafa7a1f4ec46b9eb3595fa3a7976a0")
        if flag:
            change_agent_log.write(change_agent_skill(cno,skill_str_tmp+skill,skill_level_str_tmp+"1","2","7000005","3dafa7a1f4ec46b9eb3595fa3a7976a0")+"\n")
        else:
            change_agent_log.write("修改失败，未获取到技能"+skill_str_tmp+"\n")
        time.sleep(0.5)
    change_agent_log.close()

