import requests
import time
import hashlib
import codecs
import datetime
import os
import json
import urllib


def get_sign(enterprise_id, token, timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def create_skill(url_host, skill_name, enterprise_id, token):
    url = url_host + "interface/v10/skill/create"
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params = {
        "enterpriseId": enterprise_id,
        "validateType": 2,
        "name": skill_name,
        "comment": skill_name,
        "timestamp": timestamp,
        "sign": sign_md5
    }
    r = requests.post(url, params)
    result_str = str(r.json())
    result_str = str(params)+"--------"+result_str
    try:
        skill_id = r.json()["data"]["id"]
        return skill_id, result_str
    except Exception:
        return 0, result_str


def create_queue(url_host, qno, queuename, skill_id, enterprise_id, token):
    params = {
        "queue": {
            "qno": qno,
            "enterpriseId": enterprise_id,
            "description": queuename,
            "maxLen": "0",
            "memberTimeout": "25",
            "queueTimeout": "120",
            "strategy": "rrordered",
            "musicClass": "default",
            "sayAgentno": "false",
            "wrapupTime": "3",
            "retry": "5",
            "weight": "1",
            "serviceLevel": "10",
            "vipSupport": "1",
            "joinEmpty": "1",
            "announceSound": "0",
            "announcePosition": "0"
        },
        "queueSkills": [
            {
                "skillId": skill_id,
                "skillLevel": "1"
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    create_queue_url = url_host + "interface/v10/queue/create?validateType=2&enterpriseId=" + enterprise_id + "&timestamp=" + str(
        timestamp) + "&sign=" + sign_md5
    r = requests.post(create_queue_url, headers=headers, data=json.dumps(params))
    result_str = str(r.json())
    result_str = str(params)+"--------"+result_str
    try:
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def create_agent(url_host, cno, name, area_code, hot_line, skill_ids, enterprise_id, token):
    create_agent_url = url_host + "/interface/v10/agent/create"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        "areaCode": area_code,
        "wrapup": 3,
        "skillIds": skill_ids,
        "skillLevels": 1,
        "cno": cno,
        "name": name,
        "obClidType": 2,
        "obClid": str(area_code) + str(hot_line)
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    r = requests.post(create_agent_url, params)
    result_str = str(r.json())
    result_str = str(params)+"--------"+result_str
    try:
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def create_gateway(url_host,name,password, enterprise_id, token):
    create_gateway_url = url_host + "/interface/v10/iad/create"
    result_str = "调接口失败"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        "name": name,
        "password": password,
        "allow": "alaw,ulaw",
        "registerLimit": 20,
        "comment": name,
        "deviceType": "DAG2000"
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    try:
        r = requests.post(create_gateway_url, params)
        result_str = str(r.json())
        result_str = str(params)+"--------"+result_str
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def create_extension(url_host,exten,password,area_code,iad_name, enterprise_id, token):
    create_extension_url = url_host + "/interface/v10/exten/create"
    result_str = "调接口失败"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        "exten": exten,
        "password": password,
        "allow": "alaw,ulaw,g729",
        "areaCode": area_code,
        "type": 1,
        "iadName": iad_name
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    try:
        r = requests.post(create_extension_url, params)
        result_str = str(r.json())
        result_str = str(params) + "--------" + result_str
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def create_webrtc(url_host, webrtc_num, area_code, enterprise_id, token):
    create_webrtc_url = url_host + "/interface/v10/exten/create"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'exten': webrtc_num,
        'password': '8888',
        'areaCode': area_code,
        'type': 2,
        'allow': "alaw,ulaw"
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    r = requests.post(create_webrtc_url, params)
    result_str = str(r.json())
    result_str = str(params) + "--------" + result_str
    try:
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def create_personnel(url_host, crmId, name, cno, enterprise_id, token,pwd):
    if pwd == "":
        pwd = "fde8baf43180070c05b35b63405dbe84"
    create_personnel_url = url_host + "/interface/v10/personnel/create"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'crmId': crmId,
        'name': name,
        'pwd': pwd,
        'cno': cno,
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    r = requests.post(create_personnel_url, params)
    result_str = str(r.json())
    result_str = str(params) + "--------" + result_str
    try:
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def import_ivr(url_host, new_file, enterprise_id, token):
    files = {"file": open(new_file, "rb")}
    import_ivr_url = url_host + "/interface/v10/ivrProfile/import?"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    param_str = urllib.parse.urlencode(params)  # urlencode参数
    import_ivr_url = import_ivr_url + param_str
    r = requests.post(import_ivr_url, files=files)
    result_str = str(r.json())
    result_str = str(params) + "--------" + result_str
    try:
        if str(r.json()["result"]) == "0":
            return True, result_str
    except Exception:
        pass
    return False, result_str


def create_router(url_host, enterprise_id, token):
    get_ivr_url = url_host + "/interface/v10/ivrProfile/list"
    create_router_url = url_host + "/interface/v10/ivrRouter/create"
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        "routerType":1,
        "priority":999
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    params["timestamp"] = timestamp
    params["sign"] = sign_md5
    ivr_r = requests.post(get_ivr_url, params)
    result_str = str(ivr_r.json())
    result_str = str(params) + "--------" + result_str
    try:
        if str(ivr_r.json()["result"]) == "0":
            ivr_id = ivr_r.json()["data"][0]["id"]
            params["ivrId"] = ivr_id
            router_r = requests.post(create_router_url, params)
            result_str = str(router_r.json())
            result_str = str(params) + "--------" + result_str
            try:
                if str(router_r.json()["result"]) == "0":
                    return True, result_str
            except Exception:
                pass
            return False, result_str
    except Exception:
        pass
    return False, result_str


def import_push(url_host, enterprise_id, token):
    path_list = ["1.txt","2.txt","3.txt","4.txt",]
    result_str = ""
    tmp = "调接口失败"
    for path_str in path_list:
        files = {"file": open("D:\gq/"+path_str, "rb")}
        params = {
            'validateType': 2,
            "enterpriseId": enterprise_id,
        }
        timestamp = int(time.time())
        sign_md5 = get_sign(enterprise_id, token, timestamp)
        params["timestamp"] = timestamp
        params["sign"] = sign_md5
        param_str = urllib.parse.urlencode(params)  # urlencode参数
        import_push_url = url_host + "/interface/v10/enterprisePushAction/importPush?" + param_str
        tmp = ""
        try:
            r = requests.post(import_push_url, files=files)
            result_str = result_str + str(params) + "--------" + result_str+";"
            if str(r.json()["result"]) != "0":
                tmp = tmp+path_str+"导入失败;"
            else:
                tmp = tmp + path_str + "导入成功;"
        except Exception:
                tmp = tmp+path_str+"导入失败;"
        result_str = tmp +result_str
    return result_str


if __name__ == "__main__":
    data_resource = codecs.open(r"D:\gq/1.csv", 'r', 'utf-8-sig')
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    log_path = "D:\gq/log/" + today_str + "/"  # 定义日志存放地址，默认为当前文件同目录下log文件夹下
    tmp_path = "D:\gq/tmp/" + today_str + "/"  # 定义临时字典存放地址，默认为当前文件同目录下tmp文件夹下
    ivr_path = "D:\gq/ivr/" + today_str + "/"  # 定义临时ivr存放地址，默认为当前文件同目录下ivr文件夹下
    yongyou_path = "D:\gq/yongyou/" + today_str + "/"  # 定义临时ivr存放地址，默认为当前文件同目录下ivr文件夹下
    url_host = "https://interface-gqcq.gacmotor.com/"
    # url_host = "https://api-test-2.cticloud.cn/"
    if not os.path.exists(log_path):  # 判断日志地址是否存在，若不存在则创建
        os.makedirs(log_path)
    if not os.path.exists(tmp_path):  # 判断缓存地址是否存在，若不存在则创建
        os.makedirs(tmp_path)
    if not os.path.exists(ivr_path):  # 判断ivr地址是否存在，若不存在则创建
        os.makedirs(ivr_path)
    if not os.path.exists(yongyou_path):  # 判断ivr地址是否存在，若不存在则创建
        os.makedirs(yongyou_path)
    skill_tmp_resource = ""
    queue_tmp_resource = ""
    transfer_tmp_resource = ""
    skill_dict = {}
    queue_dict = {}
    transfer_dict = {}
    gateway_dict = {}
    mendian_dict = json.load(open("D:\gq/mendian.json", encoding='utf-8'))
    try:
        skill_dict = json.load(open(tmp_path + "skill.json", encoding='utf-8'))
        queue_dict = json.load(open(tmp_path + "queue.json", encoding='utf-8'))
        transfer_dict = json.load(open(tmp_path + "transfer.json", encoding='utf-8'))
        gateway_dict = json.load(open(tmp_path + "gateway.json", encoding='utf-8'))
    except Exception:
        print(Exception.__context__)
    result_log_source = codecs.open(log_path + "result.log", 'a+', 'utf-8')
    skill_log_source = codecs.open(log_path + "skill.log", 'a+', 'utf-8')
    queue_log_source = codecs.open(log_path + "queue.log", 'a+', 'utf-8')
    agent_log_source = codecs.open(log_path + "agent.log", 'a+', 'utf-8')
    personnel_log_source = codecs.open(log_path + "personnel.log", 'a+', 'utf-8')
    gateway_log_source = codecs.open(log_path + "gateway.log", 'a+', 'utf-8')
    extension_log_source = codecs.open(log_path + "extension.log", 'a+', 'utf-8')
    webrtc_log_source = codecs.open(log_path + "webrtc.log", 'a+', 'utf-8')
    ivr_log_source = codecs.open(log_path + "ivr.log", 'a+', 'utf-8')
    push_log_source = codecs.open(log_path + "push.log", 'a+', 'utf-8')
    router_log_source = codecs.open(log_path + "router.log", 'a+', 'utf-8')
    yongyou_data_source = codecs.open(yongyou_path + today_str+".csv", 'w+', 'utf-8-sig')
    try:
        for data in data_resource:
            data_list = data.replace("\r", "").replace("\n", "").split(",")
            name = data_list[0]  # 座席、员工姓名
            skill_name = data_list[1]  # 技能名称
            personnel_id = data_list[2]  # 员工id
            area_code = data_list[3]  # 区号
            hot_line = data_list[4]  # 热线号码
            personnel_pwd = data_list[5]  # 员工密码
            enterprise_id = data_list[6]  # 呼叫中心编号
            token = data_list[7]  # token
            cno = data_list[8]  # 座席号
            extension_num = "2"+cno[1:]
            extension_pwd = data_list[9]  # 分机密码
            iad_name = data_list[10]  # iad名称
            iad_pwd = data_list[11]  # iad密码
            num = data_list[12]  # 序号
            unique_num = data_list[13]  # 门店编号
            try:
                int(num)
            except Exception:
                continue
            print(num)
            result_log_source.write(str(num))
            try:
                skills_map = skill_dict[enterprise_id]
            except Exception:
                skill_dict[enterprise_id] = {}
            try:
                queues_map = queue_dict[enterprise_id]
            except Exception:
                queue_dict[enterprise_id] = {}
            try:
                transfers_map = transfer_dict[enterprise_id]
            except Exception:
                transfer_dict[enterprise_id] = {}
            try:
                gateways_map = gateway_dict[enterprise_id]
            except Exception:
                gateway_dict[enterprise_id] = {}
            skill_id = 0
            transfer_dict[enterprise_id]["code"] = unique_num
            transfer_dict[enterprise_id]["token"] = token
            try:
                transfer_map = transfer_dict[enterprise_id]["persons"]
            except Exception:
                transfer_dict[enterprise_id]["persons"] = {}
            transfer_dict[enterprise_id]["persons"][cno] = str(cno) + "," + str(personnel_id) + ",," + str(
                cno) + ",," + str(personnel_id) + "," + str(name) + "," + str(skill_name) + "," + str(unique_num) + "\n"
            try:
                skill_id = skill_dict[enterprise_id][skill_name]
                result_log_source.write(";获取技能成功")
            except Exception:
                skill_id, skill_result_str = create_skill(url_host, skill_name, enterprise_id, token)
                skill_log_source.write(str(num) + ";" + skill_result_str + "\n")
                if skill_id == 0:
                    result_log_source.write(";创建技能失败\n")
                    continue
                else:
                    result_log_source.write(";创建技能成功")
                    skill_dict[enterprise_id][skill_name] = skill_id
            tmp_next_qno = 1001
            try:
                queues_map = queue_dict[enterprise_id]["queue"][skill_name]
                result_log_source.write(";获取队列成功")
            except Exception:
                try:
                    tmp_next_qno = int(queue_dict[enterprise_id]["next_qno"])
                except Exception:
                    pass
                queue_flag, queue_result_str = create_queue(url_host, str(tmp_next_qno), skill_name, skill_id, enterprise_id,
                                                            token)
                queue_log_source.write(str(num) + ";" + queue_result_str + "\n")
                if queue_flag:
                    queue_dict[enterprise_id]["next_qno"] = tmp_next_qno + 1
                    try:
                        queues_map = queue_dict[enterprise_id]["queue"]
                    except Exception:
                        queue_dict[enterprise_id]["queue"] = {}
                    queue_dict[enterprise_id]["queue"][skill_name] = tmp_next_qno
                    result_log_source.write(";创建队列成功")
                else:
                    result_log_source.write(";创建队列失败")
            agent_flag, agent_result_str = create_agent(url_host, cno, name, area_code, hot_line, skill_id,
                                                        enterprise_id, token)
            agent_log_source.write(str(num) + ";" + agent_result_str + "\n")
            if agent_flag:
                result_log_source.write(";创建座席成功")
            else:
                result_log_source.write(";创建座席失败")
            try:
                transfer_map = transfer_dict[enterprise_id]["list"]
            except Exception:
                transfer_dict[enterprise_id]["list"] = {}
            transfer_dict[enterprise_id]["list"][cno] = hot_line
            webrtc_flag, webrtc_result_str = create_webrtc(url_host, cno, area_code, enterprise_id, token)
            webrtc_log_source.write(str(num) + ";" + webrtc_result_str + "\n")
            if webrtc_flag:
                result_log_source.write(";创建webrtc成功")
            else:
                result_log_source.write(";创建webrtc失败")
            try:
                gateway_pwd_tmp = gateway_dict[enterprise_id][iad_name]
                result_log_source.write(";获取网关成功")
            except Exception:
                gateway_flag, gateway_result_str = create_gateway(url_host,iad_name,iad_pwd,enterprise_id,token)
                gateway_log_source.write(str(num) + ";" + gateway_result_str + "\n")
                if gateway_flag:
                    gateway_dict[enterprise_id][iad_name] = iad_pwd
                    result_log_source.write(";创建网关成功")
                else:
                    result_log_source.write(";创建网关失败")
            extension_flag, extension_result_str = create_extension(url_host,extension_num,extension_pwd,area_code,iad_name,enterprise_id,token)
            extension_log_source.write(str(num) + ";" + extension_result_str + "\n")
            if extension_flag:
                result_log_source.write(";创建分机成功")
            else:
                result_log_source.write(";创建分机失败")
            personnel_flag, personnel_result_str = create_personnel(url_host, personnel_id, name, cno, enterprise_id,
                                                                    token,personnel_pwd)
            personnel_log_source.write(str(num) + ";" + personnel_result_str + "\n")
            if personnel_flag:
                result_log_source.write(";创建员工成功\n")
            else:
                result_log_source.write(";创建员工失败\n")
    except Exception:
        result_log_source.write("\n")
        raise Exception
    finally:
        json.dump(skill_dict, open(tmp_path + "skill.json", "w", encoding='utf-8'))
        json.dump(queue_dict, open(tmp_path + "queue.json", "w", encoding='utf-8'))
        json.dump(transfer_dict, open(tmp_path + "transfer.json", "w", encoding='utf-8'))
        json.dump(gateway_dict, open(tmp_path + "gateway.json", "w", encoding='utf-8'))
        extension_log_source.close()
        gateway_log_source.close()
        personnel_log_source.close()
        agent_log_source.close()
        queue_log_source.close()
        skill_log_source.close()
        data_resource.close()
    yongyou_data_str = ""
    ivr_resource = codecs.open(r"D:\gq/ivr/template.txt", 'r', 'utf-8')
    try:
        for enterprise_key in transfer_dict:
            yongyou_data_str = yongyou_data_str + str(mendian_dict[transfer_dict[enterprise_key]["code"]]) + ",坐席号,CTI员工号,密码（明文：gqcq@2020）,绑定分机号,是否有效,传祺登录账号,员工姓名,岗位,经销商代码,经销商名称\n"
            yongyou_data_count = 1
            for yongyou_data_cno_str in transfer_dict[enterprise_key]["persons"]:
                yongyou_data_str = yongyou_data_str + str(yongyou_data_count) +","+ str(transfer_dict[enterprise_key]["persons"][yongyou_data_cno_str])
                yongyou_data_count += 1
            yongyou_data_str = yongyou_data_str + "\n"
            ivr_resource = codecs.open(r"D:\gq/ivr/template.txt", 'r', 'utf-8')
            ivr_result_str = "未导入"
            try:
                new_file = ivr_path + str(enterprise_key) + ".txt"
                ivr_tmp_source = codecs.open(new_file, 'w+', 'utf-8')
                i = 0
                for tmp_str in ivr_resource:
                    if i == 4:
                        for cno_key in transfer_dict[enterprise_key]["list"]:
                            tmp_str = tmp_str.replace("{" + str(cno_key) + "}", str(transfer_dict[enterprise_key]["list"][cno_key]))
                    ivr_tmp_source.write(tmp_str)
                    i += 1
                ivr_tmp_source.close()
                ivr_flag, ivr_result_str = import_ivr(url_host, new_file, enterprise_key,
                                                      transfer_dict[enterprise_key]["token"])
                if ivr_flag:
                    ivr_log_source.write(str(enterprise_key) + ";导入ivr成功"+ivr_result_str+"\n")
                else:
                    ivr_log_source.write(str(enterprise_key) + ";导入ivr失败"+ivr_result_str+"\n")
            except Exception:
                ivr_log_source.write(str(enterprise_key) + ";导入ivr失败;"+ivr_result_str+"\n")
            ivr_resource.close()
            router_result_str = "调用创建路由方法报错"
            try:
                router_flag,router_result_str = create_router(url_host,enterprise_key,transfer_dict[enterprise_key]["token"])
                if router_flag:
                    router_log_source.write(str(enterprise_key) + ";创建路由成功;" + router_result_str + "\n")
                else:
                    router_log_source.write(str(enterprise_key) + ";创建路由失败;" + router_result_str + "\n")
            except Exception:
                router_log_source.write(str(enterprise_key) + ";创建路由失败;"+router_result_str+"\n")
            try:
                push_result_str = import_push(url_host,enterprise_key,transfer_dict[enterprise_key]["token"])
                push_log_source.write(str(enterprise_key) + push_result_str + "\n")
            except Exception:
                push_log_source.write(str(enterprise_key) + ";导入推送失败\n")
    except Exception:
        print("发生异常"+str(enterprise_key))
        pass
    finally:
        ivr_log_source.close()
        ivr_resource.close()
        router_log_source.close()
        push_log_source.close()
        yongyou_data_source.write(yongyou_data_str)
        yongyou_data_source.close()
