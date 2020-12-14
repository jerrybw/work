import json
import codecs
import datetime
import os

skill_dict = json.load(open("gq/data.json", encoding='utf-8'))
today_str = datetime.datetime.now().strftime('%Y-%m-%d')
if not os.path.exists("gq/report/"+today_str):  # 判断日志地址是否存在，若不存在则创建
    os.makedirs("gq/report/"+today_str)
data_source = codecs.open("gq/report/"+today_str+"/report.csv", 'w+', 'utf-8')
tmp = "部门名称,编号,所属机构,企业ID,外呼总数,外呼客户接听数,外呼双方接听率,来电总数,来电座席接听数,来电双方接听率,登录座席数,活跃座席数\n"
# tmp = "部门名称,企业ID,外呼总数,外呼客户接听数,登录座席数,活跃座席数\n"
for line in skill_dict["result"]:
    tmp = tmp + str(line["rowName"])+","+ str(line["stringId"])+","+ str(line["organizationName"])+","+ str(line["enterpriseId"])+","+ str(line["obTotalCount"])\
          +","+ str(line["obCustomerAnswerCount"])+","+ str(line["obAnswerRate"])+","+ str(line["ibTotalCount"])+","+ str(line["ibAgentAnswerCount"])+","\
          + str(line["ibAnswerRate"])+","+ str(line["loginedAgentCountArray"][0]) + ","+ str(line["activeAgentCountArray"][0])+"\n"
    # tmp = tmp + str(line["rowName"])+","+ str(line["enterpriseId"])+","+ str(line["obTotalCount"])\
    #       +","+ str(line["obCustomerAnswerCount"])+","+ str(line["loginedAgentCountArray"][0]) + ","+ str(line["activeAgentCountArray"][0])+"\n"
data_source.write(tmp)
data_source.close()