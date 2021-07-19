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
    data_resource = codecs.open(r"D:\zjtd/1.csv", 'r', 'utf-8')
    host = "vnc.vlink.cn"
    # host = "39.97.196.29"
    tel_a = "17674759948"
    tel_b = "01089170766"
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    result_path = "D:\zjtd/log/" + today_str + "/"
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    result_writer = codecs.open(result_path + today_str + ".csv", 'w+', 'utf-8-sig')
    bind_url = "http://"+host+"/interface/v3/axb/bindNumberGx"
    params = {
        'expiration': 3,
        'telA': tel_a,
        'telB': tel_b,
    }
    for line in data_resource:
        line_str_dict = line.replace("\r","").replace("\n","").split(",")
        timestamp = int(time.time())
        tel_x = line_str_dict[0]
        app_id = line_str_dict[1]
        token = line_str_dict[2]
        params["timestamp"] = timestamp
        params["telX"]= tel_x
        params["appId"] = app_id
        sign_md5 = get_sign(app_id, token, timestamp)
        params["sign"]=sign_md5
        bind_r = request(bind_url, params)
        tmp_str = tel_x+","+app_id
        print(bind_r.json())
        if str(bind_r.json()["result"]) == "0":
            tmp_str = tmp_str+",success,\""+str(bind_r.json())+"\"\n"
        else:
            tmp_str = tmp_str + ",fail,\"" + str(bind_r.json())+"\"\n"
        result_writer.write(tmp_str)
        time.sleep(0.5)