import datetime
import time
import hashlib
import requests
import codecs


def get_sign(enterprise_id,token,timestamp):
    hl = hashlib.md5()
    sign_str = enterprise_id + str(timestamp) + token
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest()


if __name__ == "__main__":
    enterprise_id = "7000005"
    token = "3dafa7a1f4ec46b9eb3595fa3a7976a0"
    date_str = (datetime.date.today()).strftime('%Y-%m-%d')
    url = "https://api-2.cticloud.cn/interface/v10/outboundReport/obClidReport"
    data_source = codecs.open("D:\guazi/answer_rate"+date_str+".csv", 'w+', 'utf-8-sig')
    params = {
        'validateType': 2,
        "enterpriseId": enterprise_id,
        'timestamp': 0,
        'timeRangeType': 1,
        'statisticMethod': 2,
        "limit":1000
    }
    data_source.write(",952517,10108001,10109166,A号码,固话\n")
    total_round = 15
    for i in range(total_round):
        timestamp = int(time.time())
        sign_md5 = get_sign(enterprise_id, token, timestamp)
        params["timestamp"] = timestamp
        params["sign"] = sign_md5
        days=datetime.timedelta(days=(total_round-i))
        date_str = (datetime.date.today()-days).strftime('%Y-%m-%d')
        params["startTime"] = date_str
        params["endTime"] = date_str
        print(date_str)
        get_report_r = requests.post(url, params)
        total_95_tmp = 0
        answer_95_tmp = 0
        answer_rate_95_tmp = 0
        total_10108001_tmp = 0
        answer_10108001_tmp = 0
        answer_rate_10108001_tmp = 0
        total_10109166_tmp = 0
        answer_10109166_tmp = 0
        answer_rate_10109166_tmp = 0
        total_A_tmp = 0
        answer_A_tmp = 0
        answer_rate_A_tmp = 0
        total_gh_tmp = 0
        answer_gh_tmp = 0
        answer_rate_gh_tmp = 0
        for data_str in get_report_r.json()["data"]:
            if str(data_str["clid"]) == "952517":
                total_95_tmp += int(data_str["totalCount"])
                answer_95_tmp += int(data_str["answeredCount"])
            elif str(data_str["clid"]) == "10108001":
                total_10108001_tmp += int(data_str["totalCount"])
                answer_10108001_tmp += int(data_str["answeredCount"])
            elif str(data_str["clid"]) == "10109166":
                total_10109166_tmp += int(data_str["totalCount"])
                answer_10109166_tmp += int(data_str["answeredCount"])
            elif str(data_str["trunkGroupKey"]) == "40003" or str(data_str["trunkGroupKey"]) == "50001" or str(data_str["trunkGroupKey"]) == "61079" or str(data_str["trunkGroupKey"]) == "20013":
                total_gh_tmp += int(data_str["totalCount"])
                answer_gh_tmp += int(data_str["answeredCount"])
            elif str(data_str["trunkGroupKey"]) == "10012" or str(data_str["trunkGroupKey"]) == "20034":
                total_A_tmp += int(data_str["totalCount"])
                answer_A_tmp += int(data_str["answeredCount"])
            else:
                total_gh_tmp += int(data_str["totalCount"])
                answer_gh_tmp += int(data_str["answeredCount"])
        answer_rate_95_tmp = answer_95_tmp/total_95_tmp if total_95_tmp != 0 else 0
        answer_rate_10108001_tmp = answer_10108001_tmp/total_10108001_tmp if total_10108001_tmp !=0 else 0
        answer_rate_10109166_tmp = answer_10109166_tmp/total_10109166_tmp if total_10109166_tmp !=0 else 0
        answer_rate_A_tmp = answer_A_tmp/total_A_tmp if total_A_tmp !=0 else 0
        answer_rate_gh_tmp = answer_gh_tmp/total_gh_tmp if total_gh_tmp !=0 else 0
        data_tmp = date_str+","+str(round(answer_rate_95_tmp*100,2))+"%,"+str(round(answer_rate_10108001_tmp*100,2))+"%,"+str(round(answer_rate_10109166_tmp*100,2))+"%,"+str(round(answer_rate_A_tmp*100,2))+"%,"+str(round(answer_rate_gh_tmp*100,2))+"%\n"
        # print(date_str+"：95 数据---总："+str(total_95_tmp) + "接听："+str(answer_95_tmp)+"接听率："+str(round(answer_rate_95_tmp*100,2))+"%")
        # print(date_str+"：10108001 数据---总："+str(total_10108001_tmp) + "接听："+str(answer_10108001_tmp)+"接听率："+str(round(answer_rate_10108001_tmp*100,2))+"%")
        # print(date_str+"：10109166 数据---总："+str(total_10109166_tmp) + "接听："+str(answer_10109166_tmp)+"接听率："+str(round(answer_rate_10109166_tmp*100,2))+"%")
        # print(date_str+"：A 数据---总："+str(total_A_tmp) + "接听："+str(answer_A_tmp)+"接听率："+str(round(answer_rate_A_tmp*100,2))+"%")
        # print(date_str+"：gh 数据---总："+str(total_gh_tmp) + "接听："+str(answer_gh_tmp)+"接听率："+str(round(answer_rate_gh_tmp*100,2))+"%")
        data_source.write(data_tmp)
        time.sleep(10)
    data_source.close()