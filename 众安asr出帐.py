import urllib
import requests
import time
import hashlib
import codecs
import os
import datetime
from urllib import parse


# 定义获取sign的方法，需要参数为呼叫中心编号，token，时间戳
def get_sign(enterprise_id,token,timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def get_time_str(timestamp):
    timestamp = int(timestamp)
    time_array = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def get_m(start,end):
    end = int(end)
    start = int(start)
    tmp = (end - start) // 60
    if (end-start)%60 != 0:
        tmp += 1
    return str(tmp)

# 主程序入口
'''
要求录音文件夹必须存在，默认为前文件同目录下record文件夹下，并将要上传的录音文件存放在文件夹下
运行时需要修改两个变量：enterprise_id、token，修改为真实客户的enterprise_id、toke
'''
if __name__ == "__main__":
    i = 0
    now_time = datetime.datetime.now()
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    region = "1" #定义平台
    in_url = "https://api-" + region + ".cticloud.cn/interface/v10/cdr/ib/query"
    out_url = "https://api-" + region + ".cticloud.cn/interface/v10/cdr/ob/query"
    get_queue_url = "https://api-" + region + ".cticloud.cn/interface/v10/queue/list"
    enterprise_id = "7100001" #定义呼叫中心编号
    token = "" #定义token
    month = "10"
    asr_path = "asr/"+month+"/" #定义录音文件存放位置，必须存在
    asr_result_path = "asr/"+month+"result/" #定义录音文件存放位置，必须存在
    log_path = "log/"+today_str+"/" #定义日志存放地址，默认为当前文件同目录下log文件夹下
    if not os.path.exists(log_path): #判断日志地址是否存在，若不存在则创建
        os.mkdir(log_path)
    # log_source = codecs.open(log_path+"asr.log", 'a+', 'utf-8')
    param = {
        "enterpriseId":enterprise_id,
        "validateType":2,
    }
    timestamp = int(time.time())
    sign_md5 = get_sign(enterprise_id, token, timestamp)
    param["timestamp"] = str(timestamp)
    param["sign"] = sign_md5
    r = requests.post(get_queue_url, param)
    queue_dict = {}
    for queue in r.json()["data"]["list"]:
        queue_dict[queue["qno"]] = queue["description"]
    in_source = codecs.open(asr_result_path+"asr_in_all.csv", 'a+', 'utf-8')
    in_source.write("unique_id,客户号码,热线号码,队列号,队列名,座席工号,座席姓名,座席电话,座席应答时间（asr开始时间）,结束时间（asr结束时间）,asr转写计费时长（分钟）,asr转写费用（元）\n")
    out_source = codecs.open(asr_result_path+"asr_out_all.csv", 'a+', 'utf-8')
    out_source.write("unique_id,客户号码,座席工号,座席姓名,座席电话,座席应答时间（asr开始时间）,结束时间（asr结束时间）,asr转写计费时长（分钟）,asr转写费用（元）\n")
    # total_source = codecs.open(asr_result_path + "asr_total.csv", 'a+', 'utf-8')
    # total_source.write(",条数,asr总转写计费时长（分钟）,asr转写费用（元）")
    # out_total_count = 0
    # in_total_count = 0
    # out_total_m = 0
    # in_total_m = 0
    for maindir, subdir, file_name_list in os.walk(asr_path): #遍历录音存放地址
        for f in file_name_list:
            tmp_file = os.path.join(maindir, f)
            cdr = codecs.open(tmp_file, 'r', 'utf-8')
            tmp_source = in_source
            tmp_url = in_url
            if "out" in f:
                tmp_source = out_source
                tmp_url = out_url
            else:
                tmp_source = in_source
                tmp_url = in_url
            for tmp_line in cdr:
                tmp_result = ""
                if "从通道" in tmp_line or "录音文件时长" in tmp_line:
                    continue
                timestamp = int(time.time())
                sign_md5 = get_sign(enterprise_id, token, timestamp)
                tmp_list = tmp_line.replace("\"","").split(",")
                param["timestamp"] = str(timestamp)
                param["sign"] = sign_md5
                param["uniqueId"] = tmp_list[4]
                r = requests.post(tmp_url,param)
                try:
                    bridge_time = r.json()["data"][0]["bridgeTime"]
                    end_time = r.json()["data"][0]["endTime"]
                    m = get_m(bridge_time,end_time)
                    p = int(m)*0.05
                    if "in" in f:
                        qno = r.json()["data"][0]["qno"]
                        queue_name = ""
                        if qno != "":
                            queue_name = queue_dict[r.json()["data"][0]["qno"]]
                        tmp_result = tmp_list[4]+","+r.json()["data"][0]["customerNumber"]+","+r.json()["data"][0]["hotline"]\
                                 +","+qno+","+queue_name+","+r.json()["data"][0]["cno"]+","+r.json()["data"][0]["agentName"] \
                                + "," + r.json()["data"][0]["calleeNumber"]\
                                +","+get_time_str(bridge_time)+","+get_time_str(end_time)+","+m+","+str(float('%.2f'%p))+"\n"
                        # out_total_count += 1
                        # out_total_m += int(m)
                    else:
                        tmp_result = tmp_list[4] + "," + r.json()["data"][0]["customerNumber"] + ","\
                                     + "," + r.json()["data"][0]["cno"] + "," + r.json()["data"][0]["agentName"] + "," + r.json()["data"][0]["agentNumber"]\
                                     + "," + get_time_str(bridge_time)+ "," + get_time_str(end_time) + "," + m + "," + str(float('%.2f'%p)) + "\n"
                        # in_total_count += 1
                        # in_total_m += int(m)
                except Exception:
                    tmp_result = tmp_list[4] + "," +str(r.json())+"\n"
                tmp_source.write(tmp_result)
                now_time = datetime.datetime.now()
                time1 = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
                # log_source.write(time1 + "        "+ str(r.json())+"\n")
    # total_source.write("呼入,"+str(in_total_count)+","+str(in_total_m)+","+str(float('%.2f'%(in_total_m*0.05)))+"\n")
    # total_source.write("外呼,"+str(out_total_count)+","+str(out_total_m)+","+str(float('%.2f'%(out_total_m*0.05)))+"\n")
    # total_source.write("呼入,"+str(in_total_count+out_total_count)+","+str(in_total_m+out_total_m)+","+str(float('%.2f'%((in_total_m+out_total_m)*0.05))))
    # log_source.close()
    in_source.close()
    out_source.close()
    # total_source.close()