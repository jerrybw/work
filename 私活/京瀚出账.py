import xlrd

def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(r"D:\1、工作\风时\8002596用户账单各计费项明细-2021-06.xls")
    tonghuafei = 0.0
    zuoxishu = 0
    zuoxifei = 0.0
    haomafei = 0.0
    other = 0.0
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        if sheet_name == "基本通话资费":
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                rows = sheet.row_values(i)
                tonghuafei += float(rows[5])
            print(tonghuafei)
        if sheet_name == "座席功能费":
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                rows = sheet.row_values(i)
                zuoxishu += int(rows[1])
                zuoxifei += float(rows[3])
            print(zuoxishu)
            print(zuoxifei)
        if sheet_name == "号码功能费":
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                rows = sheet.row_values(i)
                haomafei += float(rows[2])
            print(zuoxishu)
        if sheet_name == "增值业务费":
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                rows = sheet.row_values(i)
                other += float(rows[3])
            print(other)
    # 根据sheet索引或者名称获取sheet内容
    # sheet = workbook.sheet_by_index(0) # sheet索引从0开始

    print("通话费："+str(tonghuafei)+"号码功能费："+str(haomafei)+"坐席数："+str(zuoxishu)+"坐席费："+str(zuoxifei)+"总消费："+str(round(tonghuafei+zuoxifei+haomafei+other,2)))


if __name__ == '__main__':
    # 读取Excel
    read_excel();
    print ('读取成功')