import requests
import time
import hashlib
import codecs
import json


def get_md5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def send_request(dict):
    log = codecs.open(r"log/guazinumber.log", 'a+', 'utf-8')
    url = "http://go-callcenter.guazi.com/external/manage_callout_numbers"
    headers = {'Content-Type': 'application/json'}
    timestamp = int(time.time())
    dict["timestamp"] = timestamp
    secret= "NLRC5G0DWJ637LG0"
    signature_str = ""
    for key in sorted(dict):
        if type(dict[key]) == int or type(dict[key]) == str:
            signature_str = signature_str + str(dict[key])
    signature_str = signature_str+secret
    print(signature_str)
    dict["signature"]=get_md5(signature_str)
    print(get_md5(signature_str))
    print(dict)
    log.write(str(time.time())+str(dict)+"\n")
    r = requests.post(url,headers=headers,data=json.dumps(dict))
    print(r.json())
    log.write(str(r.json()))
    log.close()


#电信服务商, 0未定义, 1移动, 2联通, 3电信
if __name__ == "__main__":
    dict = {
	    "vendor":"2"
    }
    numbers = codecs.open(r"guazinumbers.csv", 'r', 'utf-8')
    online_ctd_number_list = []
    offline_ctd_number_list = []
    online_cop_number_list = []
    offline_cop_number_list = []
    online_other_number_list = []
    offline_other_number_list = []
    online_yidong_number_list = []
    offline_yidong_number_list = []
    lists = [
        [1,1,online_ctd_number_list],
        [0,1,offline_ctd_number_list],
        [1,2,online_cop_number_list],
        [0,2,offline_cop_number_list],
        [1,0,online_other_number_list],
        [0,0,offline_other_number_list],
        [1,4,online_yidong_number_list],
        [0,4,offline_yidong_number_list]
    ]
    for number in numbers:
        number_strs = number.split(",")
        number_obj = {
            "number":number_strs[2],
            "area_code":number_strs[3].replace("\n","").replace("\r","")
        }
        if "1" == str(number_strs[0]):
            if "1" == str(number_strs[1]):
                online_ctd_number_list.append(number_obj)
            elif "2" == str(number_strs[1]):
                online_cop_number_list.append(number_obj)
            elif "0" == str(number_strs[1]):
                online_other_number_list.append(number_obj)
            elif "4" == str(number_strs[1]):
                online_yidong_number_list.append(number_obj)
            else:
                print("号码类型错误")
        elif "0" == str(number_strs[0]):
            if "1" == str(number_strs[1]):
                offline_ctd_number_list.append(number_obj)
            elif "2" == str(number_strs[1]):
                offline_cop_number_list.append(number_obj)
            elif "0" == str(number_strs[1]):
                offline_other_number_list.append(number_obj)
            elif "4" == str(number_strs[1]):
                offline_yidong_number_list.append(number_obj)
            else:
                print("号码类型错误")
        else:
            print("上下线类型错误")
    numbers.close()
    for list in lists:
        if len(list[2]) > 0:
            dict["number_action"] = list[0]
            dict["ctd"] = list[1]
            dict["number_list"] = list[2]
            send_request(dict)
            dict["signature"]=""