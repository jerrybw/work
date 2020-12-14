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


# 主程序入口
'''
要求录音文件夹必须存在，默认为前文件同目录下record文件夹下，并将要上传的录音文件存放在文件夹下
运行时需要修改两个变量：enterprise_id、token，修改为真实客户的enterprise_id、toke
'''
if __name__ == "__main__":
    i = 0
    now_time = datetime.datetime.now()
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    region = "2" #定义平台
    upoad_file_url_without_param = "https://api-" + region + ".cticloud.cn/interface/v10/enterpriseVoice/create?"
    enterprise_id = "7000768" #定义呼叫中心编号
    # enterprise_id = "7100001" #定义呼叫中心编号
    token = "" #定义token
    # token = "" #定义token
    record_path = "upload/" #定义录音文件存放位置，必须存在
    log_path = "log/"+today_str+"/" #定义日志存放地址，默认为当前文件同目录下log文件夹下
    if not os.path.exists(log_path): #判断日志地址是否存在，若不存在则创建
        os.mkdir(log_path)
    log_source = codecs.open(log_path+"upload.log", 'a+', 'utf-8')
    param = {
        "enterpriseId":enterprise_id,
        "validateType":2,
    }
    for maindir, subdir, file_name_list in os.walk(record_path): #遍历录音存放地址
        for f in file_name_list:
            i += 1
            timestamp = int(time.time())
            sign_md5 = get_sign(enterprise_id, token, timestamp)
            old_file = os.path.join(maindir, f)
            new_file = os.path.join(maindir, str(i)+".wav")
            param["enterpriseId"] = enterprise_id
            param["timestamp"] = str(timestamp)
            param["sign"] = sign_md5
            param["voiceName"] = f
            param_str = urllib.parse.urlencode(param) #urlencode参数
            upoad_file_url=upoad_file_url_without_param+param_str
            os.rename(old_file,new_file) #将文件重命名为数字，否则上传时会报错，应该是服务端的问题
            files = {"file": open(new_file, "rb")}
            r = requests.post(upoad_file_url,files=files)
            now_time = datetime.datetime.now()
            time1 = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
            log_source.write(time1 + "        "+ str(r.json())+"\n")
    log_source.close()