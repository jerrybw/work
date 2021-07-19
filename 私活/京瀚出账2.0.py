import xlrd
import codecs

def read_excel():
    # 打开文件
    data_resource = codecs.open(r"D:\1、工作\风时\座席列表_8002596_20210707_153600.csv", 'r')
    cno_map = {}
    zz = 0.0
    wh = 0.0
    tj = 0.0
    gz = 0.0
    cd = 0.0
    ty = 0.0
    cq = 0.0
    jn = 0.0
    km = 0.0
    dl = 0.0
    hf = 0.0
    xa = 0.0
    bj = 0.0
    cs = 0.0
    zbsc = 0.0
    for line in data_resource:
        list_list = line.split(",")
        cno = list_list[1][4:8]
        print(list_list[3])
        if "郑州" in list_list[3]:
            cno_map[cno] = "郑州"
            continue
        if "武汉" in list_list[3]:
            cno_map[cno] = "武汉"
            continue
        if "天津" in list_list[3]:
            cno_map[cno] = "天津"
            continue
        if "广州" in list_list[3]:
            cno_map[cno] = "广州"
            continue
        if "成都" in list_list[3]:
            cno_map[cno] = "成都"
            continue
        if "太原" in list_list[3]:
            cno_map[cno] = "太原"
            continue
        if "重庆" in list_list[3]:
            cno_map[cno] = "重庆"
            continue
        if "济南" in list_list[3]:
            cno_map[cno] = "济南"
            continue
        if "昆明" in list_list[3]:
            cno_map[cno] = "昆明"
            continue
        if "大连" in list_list[3]:
            cno_map[cno] = "大连"
            continue
        if "合肥" in list_list[3]:
            cno_map[cno] = "合肥"
            continue
        if "西安" in list_list[3]:
            cno_map[cno] = "西安"
            continue
        if "总部市场" in list_list[3]:
            cno_map[cno] = "总部市场"
            continue
        elif "北京" in list_list[3]:
            cno_map[cno] = "北京"
            continue
        if "长沙" in list_list[3]:
            cno_map[cno] = "长沙"
            continue
    workbook = xlrd.open_workbook(r"D:\1、工作\风时\座席话费统计.xls")
    # workbook = xlrd.open_workbook(r"D:\1、工作\风时\8002596用户账单各计费项明细-2021-06.xls")
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        for i in range(sheet.nrows):
            if i == 0:
                continue
            rows = sheet.row_values(i)
            cno = rows[1]
            try:
                if cno_map[cno] == "郑州":
                    zz = zz + float(rows[2]) +  float(rows[3])+ float(rows[4])+ float(rows[5])
                    continue
                if cno_map[cno] == "武汉":
                    wh = wh + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "天津":
                    tj = tj + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "广州":
                    gz = gz + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "成都":
                    cd = cd + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "太原":
                    ty = ty + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "重庆":
                    cq = cq + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "济南":
                    jn = jn + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "昆明":
                    km = km + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "大连":
                    dl = dl + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "合肥":
                    hf = hf + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "西安":
                    xa = xa + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "总部市场":
                    zbsc = zbsc + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "北京":
                    bj = bj + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
                if cno_map[cno] == "长沙":
                    cs = cs + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                    continue
            except:
                bj = bj + float(rows[2]) + float(rows[3]) + float(rows[4]) + float(rows[5])
                continue
    print("郑州," + str(round(zz, 2)))
    print("武汉," + str(round(wh, 2)))
    print("天津," + str(round(tj, 2)))
    print("广州," + str(round(gz, 2)))
    print("成都," + str(round(cd, 2)))
    print("太原," + str(round(ty, 2)))
    print("重庆," + str(round(cq, 2)))
    print("济南," + str(round(jn, 2)))
    print("昆明," + str(round(km, 2)))
    print("大连," + str(round(dl, 2)))
    print("合肥," + str(round(hf, 2)))
    print("西安," + str(round(xa, 2)))
    print("北京," + str(round(bj, 2)))
    print("长沙," + str(round(cs, 2)))
    print("总部市场," + str(round(zbsc, 2)))
    print("总计," + str(round(zz + wh + tj + gz + cd + ty + cq + jn + km + dl + hf + xa + bj + cs + zbsc, 2)))


if __name__ == '__main__':
    # 读取Excel
    read_excel();
    print ('读取成功')