import json
import codecs
import datetime
import os
import requests

cookies={'SESSION':'df82c897-0996-47d8-9819-f244da816f37'}
headers = {'Content-Type': 'application/json'}
oneday=datetime.timedelta(days=1)
yesterday_str = (datetime.date.today()-oneday).strftime('%Y-%m-%d')
url = "https://home-gqcq.gacmotor.com/v1/report/tenancy/workload/list/department"
params = {
    "currentPageNo":1,
    "departmentId":"",
    "organizationId":"",
    "tenancyId":"TCC1000002",
    "pageSize":1000,
    "rptQueryCondition":{"startTime":yesterday_str,"endTime":yesterday_str,"timeRangeType":"1"}
}
get_url_r = requests.post(url,headers=headers,data=json.dumps(params),cookies=cookies)
if not os.path.exists("D:\gq/report"):  # 判断日志地址是否存在，若不存在则创建
    os.makedirs("D:\gq/report")
data_source = codecs.open("gq/report/"+yesterday_str+".csv", 'w+', 'utf-8')
tmp = "部门名称,编号,所属机构,企业ID,外呼总数,外呼客户接听数,外呼双方接听率,来电总数,来电座席接听数,来电双方接听率,登录座席数,活跃座席数\n"
# tmp = "部门名称,企业ID,外呼总数,外呼客户接听数,登录座席数,活跃座席数\n"
for line in get_url_r.json()["result"]:
    tmp = tmp + str(line["rowName"])+","+ str(line["stringId"])+","+ str(line["organizationName"])+","+ str(line["enterpriseId"])+","+ str(line["obTotalCount"])\
          +","+ str(line["obCustomerAnswerCount"])+","+ str(line["obAnswerRate"])+","+ str(line["ibTotalCount"])+","+ str(line["ibAgentAnswerCount"])+","\
          + str(line["ibAnswerRate"])+","+ str(line["loginedAgentCountArray"][0]) + ","+ str(line["activeAgentCountArray"][0])+"\n"
    # tmp = tmp + str(line["rowName"])+","+ str(line["enterpriseId"])+","+ str(line["obTotalCount"])\
    #       +","+ str(line["obCustomerAnswerCount"])+","+ str(line["loginedAgentCountArray"][0]) + ","+ str(line["activeAgentCountArray"][0])+"\n"
data_source.write(tmp)
data_source.close()