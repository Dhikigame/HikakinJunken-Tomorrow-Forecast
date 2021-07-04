# coding:utf-8
import io,sys
import csv
import platform
import os
import MySQLdb
from datetime import datetime
sys.path.append('..')
from info.information import Information


def data_parse_write5():
    # Mysqlに接続して取得したデータを挿入・更新する
    os_system = platform.system()
    if "Darwin" in os_system:
        con = MySQLdb.connect(unix_socket=Information.db_socket("Darwin"),user=Information.db_user("Darwin"),passwd=Information.db_passwd("Darwin"),host=Information.db_host("Darwin"),db=Information.db_name("Darwin"),use_unicode=Information.use_unicode("Darwin"),charset=Information.charset("Darwin"))
        if os.path.exists(Information.csv_dir("Darwin")) is True:
            os.remove(Information.csv_dir("Darwin"))
        os_path = Information.csv_dir("Darwin")
    else:
        con = MySQLdb.connect(unix_socket=Information.db_socket("Linux"),user=Information.db_user("Linux"),passwd=Information.db_passwd("Linux"),host=Information.db_host("Linux"),db=Information.db_name("Linux"),use_unicode=Information.use_unicode("Linux"),charset=Information.charset("Linux"))
        if os.path.exists(Information.csv_dir("Linux")) is True:
            os.remove(Information.csv_dir("Linux"))
        os_path = Information.csv_dir("Linux")
    cursor = con.cursor()

    sql = 'select result, upload_date from hikakin_junken_data where result != "休み" AND upload_date >= "2014-11-03" order by upload_date asc'
    cursor.execute(sql)
    get_junkendata : list = cursor.fetchall()

    junkencount : int = 0
    junkendata_result = list()
    junkendata_month = list()
    junkendata_date = list()
    junkendata_day = list()
    junkendata_date_sub = list()
    junkendata_before_result_1 = list()
    junkendata_before_result_2 = list()
    junkendata_before_result_3 = list()
    count : int = 0
    for junkencount in range(3, len(get_junkendata)):
        junkendata_before_result_1.append(junken_str_conv(get_junkendata[junkencount - 1][0]))
        junkendata_before_result_2.append(junken_str_conv(get_junkendata[junkencount - 2][0]))
        junkendata_before_result_3.append(junken_str_conv(get_junkendata[junkencount - 3][0]))
        junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

        junkendata_date.append(get_junkendata[junkencount][1])
        junkendata_month.append(date_month_split(junkendata_date[count]))
        junkendata_day.append(date_day_split(junkendata_date[count]))
        day_sub = get_junkendata[junkencount][1] - get_junkendata[junkencount - 1][1]
        junkendata_date_sub.append(day_sub.days)

        # print("------------------------------")
        # print("じゃんけん：" + junken_num_conv(junkendata_result[count]))
        # print("日付：" + str(junkendata_date[count]))
        # print("月：" + str(junkendata_month[count]))
        # print("日：" + str(junkendata_day[count]))
        # print("前回からの日数経過：" + str(junkendata_date_sub[count]))
        # print("前回のじゃんけん：" + junken_num_conv(junkendata_before_result_1[count]))
        # print("前々回のじゃんけん：" + junken_num_conv(junkendata_before_result_2[count]))
        # print("前々々回のじゃんけん：" + junken_num_conv(junkendata_before_result_3[count]))

        # 数値変換したデータをcsvファイルへ書き込み
        with open(os_path, 'a') as write_file:
            writer = csv.writer(write_file)
            writer.writerow([junkendata_result[count], 
                            junkendata_day[count], 
                            junkendata_date_sub[count], 
                            junkendata_before_result_1[count], 
                            junkendata_before_result_2[count],
                            junkendata_before_result_3[count]])
        count = count + 1

    cursor.close()
    con.close()

# じゃんけんの結果を数値変換
def junken_str_conv(result : str):
    # じゃんけんの手(数字)
    rock_num = 0        # グー
    paper_num = 1       # パー
    scissors_num = 2    # チョキ

    if result == "グー":
        result_num : int = rock_num
    if result == "パー":
        result_num : int = paper_num
    if result == "チョキ":
        result_num : int = scissors_num
    return result_num

# じゃんけんの結果を文字変換
def junken_num_conv(result : int):
    # じゃんけんの手(文字)
    rock_str = "グー"        # グー
    paper_str = "パー"       # パー
    scissors_str = "チョキ"    # チョキ

    if result == 0:
        result_str : str = rock_str
    if result == 1:
        result_str : str = paper_str
    if result == 2:
        result_str : str = scissors_str
    return result_str

# 年月日の月を切り取り
def date_month_split(date : str):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    return date.month
# 年月日の日を切り取り
def date_day_split(date : str):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    return date.day
