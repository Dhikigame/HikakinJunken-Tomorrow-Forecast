# coding:utf-8
import io,sys
import csv
import platform
import os
import MySQLdb
from datetime import datetime
sys.path.append('..')
from info.information import Information


def data_parse_write2():
    # Unicodeからutf-8へ変換
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
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

    # sql = 'select result, upload_date from hikakin_junken_data where result != "休み" order by upload_date asc'
    sql = 'select result, upload_date from hikakin_junken_data where result != "休み" AND upload_date >= "2018-01-01" order by upload_date asc'
    cursor.execute(sql)
    get_junkendata : list = cursor.fetchall()

    junkencount : int = 0
    junkendata_result = list()
    junkendata_date = list()
    junkendata_month = list()
    junkendata_day = list()
    junkendata_date_sub = list()
    junkendata_before_result_1 = list()
    junkendata_before_result_2 = list()
    for junkencount in range(0, len(get_junkendata)):
        if junkencount == 0:
            junkendata_before_result_1.append(0)
            junkendata_before_result_2.append(0)
            junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

            junkendata_date.append(get_junkendata[junkencount][1])
            junkendata_month.append(date_month_split(junkendata_date[junkencount]))
            junkendata_day.append(date_day_split(junkendata_date[junkencount]))
            junkendata_date_sub.append(0)
            date_before_1 = junkendata_date[junkencount]
            result_before_1 = junkendata_result[junkencount]
        if junkencount == 1:
            junkendata_before_result_1.append(result_before_1)
            junkendata_before_result_2.append(0)
            junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

            junkendata_date.append(get_junkendata[junkencount][1])
            junkendata_month.append(date_month_split(junkendata_date[junkencount]))
            junkendata_day.append(date_day_split(junkendata_date[junkencount]))
            day_sub = get_junkendata[junkencount][1] - date_before_1
            junkendata_date_sub.append(day_sub.days)
            date_before_2, date_before_1 = date_before_1, junkendata_date[junkencount]
            result_before_2, result_before_1 = result_before_1, junkendata_result[junkencount]
        if junkencount >= 2:
            junkendata_before_result_1.append(result_before_1)
            junkendata_before_result_2.append(result_before_2)
            junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

            junkendata_date.append(get_junkendata[junkencount][1])
            junkendata_month.append(date_month_split(junkendata_date[junkencount]))
            junkendata_day.append(date_day_split(junkendata_date[junkencount]))
            day_sub = get_junkendata[junkencount][1] - date_before_1
            junkendata_date_sub.append(day_sub.days)
            date_before_2, date_before_1 = date_before_1, junkendata_date[junkencount]
            result_before_2, result_before_1 = result_before_1, junkendata_result[junkencount]

        print("------------------------------")
        print("じゃんけん：" + junken_num_conv(junkendata_result[junkencount]))
        print("日付：" + str(junkendata_date[junkencount]))
        print("月：" + str(junkendata_month[junkencount]))
        print("日：" + str(junkendata_day[junkencount]))
        print("前回からの日数経過：" + str(junkendata_date_sub[junkencount]))
        print("前回のじゃんけん：" + junken_num_conv(junkendata_before_result_1[junkencount]))
        print("前々回のじゃんけん：" + junken_num_conv(junkendata_before_result_2[junkencount]))

        # 数値変換したデータをcsvファイルへ書き込み
        with open(os_path, 'a') as write_file:
            writer = csv.writer(write_file)
            writer.writerow([junkendata_result[junkencount], 
                            junkendata_month[junkencount], 
                            junkendata_day[junkencount], 
                            junkendata_date_sub[junkencount], 
                            junkendata_before_result_1[junkencount], 
                            junkendata_before_result_2[junkencount]])

    write_file.close()
    cursor.close()
    con.close()

# じゃんけんの結果を文字変換
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
# じゃんけんの結果を数値変換
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
