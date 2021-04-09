import csv
import platform
import calendar
import os
import MySQLdb
from datetime import datetime
sys.path.append('..')
from info.information import Information


# じゃんけんの手(数字)
rock_num = 0        # グー
paper_num = 1       # パー
scissors_num = 2    # チョキ
# じゃんけんの手(文字)
rock_str = "グー"        # グー
paper_str = "パー"       # パー
scissors_str = "チョキ"    # チョキ


# 年月日が月の第何週か求める
def get_nth_week(date, firstweekday=6):
    year = date_year_split(date)
    month = date_month_split(date)
    day = date_day_split(date)
    # calendar.monthrange:指定された月の一日の曜日と日数を返す
    first_dow = calendar.monthrange(int(year), int(month))[0]
    offset = (first_dow - int(firstweekday)) % 7
    return (int(day) + offset - 1) // 7 + 1


# 年月日の月を切り取り
def date_year_split(date : str):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    return date.year
def date_month_split(date : str):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    return date.month
# 年月日の日を切り取り
def date_day_split(date : str):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    return date.day


# じゃんけんの結果を文字変換
def junken_str_conv(result : str):
    if result == "グー":
        result_num : int = rock_num
    if result == "パー":
        result_num : int = paper_num
    if result == "チョキ":
        result_num : int = scissors_num
    return result_num
# じゃんけんの結果を数値変換
def junken_num_conv(result : int):
    if result == 0:
        result_str : str = rock_str
    if result == 1:
        result_str : str = paper_str
    if result == 2:
        result_str : str = scissors_str
    return result_str


# Mysqlに接続して取得したデータを挿入・更新する
os_system = platform.system()
if "Darwin" in os_system:
    con = MySQLdb.connect(unix_socket=Information.db_socket("Darwin"),user=Information.db_user("Darwin"),passwd=Information.db_passwd("Darwin"),host=Information.db_host("Darwin"),db=Information.db_name("Darwin"),use_unicode=Information.use_unicode("Darwin"),charset=Information.charset("Darwin"))
    if os.path.exists('Hikakin_Junken_Data.csv') is True:
        os.remove('Hikakin_Junken_Data.csv')
else:
    con = MySQLdb.connect(unix_socket=Information.db_socket("Linux"),user=Information.db_user("Linux"),passwd=Information.db_passwd("Linux"),host=Information.db_host("Linux"),db=Information.db_name("Linux"),use_unicode=Information.use_unicode("Linux"),charset=Information.charset("Linux"))
cursor = con.cursor()

# sql = 'select result, upload_date from hikakin_junken_data where result != "休み" order by upload_date asc'
sql = 'select result, upload_date from hikakin_junken_data where result != "休み" AND upload_date >= "2018-01-01" order by upload_date asc'
cursor.execute(sql)
get_junkendata : list = cursor.fetchall()

junkencount : int = 0
junkendata_result = list()
# junkendata_date = list()
junkendata_month = list()
# junkendata_day = list()
junkendata_nthweek = list()
# junkendata_date_sub = list()
junkendata_before_result_1 = list()
junkendata_before_result_2 = list()
for junkencount in range(0, len(get_junkendata)):
    if junkencount == 0:
        junkendata_before_result_1.append(0)
        junkendata_before_result_2.append(0)
        junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

        junkendata_nthweek.append(get_nth_week(get_junkendata[junkencount][1]))
        junkendata_month.append(date_month_split(get_junkendata[junkencount][1]))
        # junkendata_day.append(date_day_split(junkendata_date[junkencount]))
        # junkendata_date_sub.append(0)
        # date_before_1 = junkendata_date[junkencount]
        result_before_1 = junkendata_result[junkencount]
    if junkencount == 1:
        junkendata_before_result_1.append(result_before_1)
        junkendata_before_result_2.append(0)
        junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

        # junkendata_date.append(get_junkendata[junkencount][1])
        junkendata_nthweek.append(get_nth_week(get_junkendata[junkencount][1]))
        junkendata_month.append(date_month_split(get_junkendata[junkencount][1]))
        # junkendata_day.append(date_day_split(junkendata_date[junkencount]))
        # day_sub = get_junkendata[junkencount][1] - date_before_1
        # junkendata_date_sub.append(day_sub.days)
        # date_before_2, date_before_1 = date_before_1, junkendata_date[junkencount]
        result_before_2, result_before_1 = result_before_1, junkendata_result[junkencount]
    if junkencount >= 2:
        junkendata_before_result_1.append(result_before_1)
        junkendata_before_result_2.append(result_before_2)
        junkendata_result.append(junken_str_conv(get_junkendata[junkencount][0]))

        # junkendata_date.append(get_junkendata[junkencount][1])
        junkendata_nthweek.append(get_nth_week(get_junkendata[junkencount][1]))
        junkendata_month.append(date_month_split(get_junkendata[junkencount][1]))
        # junkendata_day.append(date_day_split(junkendata_date[junkencount]))
        # day_sub = get_junkendata[junkencount][1] - date_before_1
        # junkendata_date_sub.append(day_sub.days)
        # date_before_2, date_before_1 = date_before_1, junkendata_date[junkencount]
        result_before_2, result_before_1 = result_before_1, junkendata_result[junkencount]

    print("------------------------------")
    print("じゃんけん：" + junken_num_conv(junkendata_result[junkencount]) + str(junkendata_result[junkencount]))
    print("日付：" + str(get_junkendata[junkencount][1]))
    print("月の第何週？：" + str(junkendata_nthweek[junkencount]))
    # print("前回からの日数経過：" + str(junkendata_date_sub[junkencount]))
    print("前回のじゃんけん：" + junken_num_conv(junkendata_before_result_1[junkencount]) + str(junkendata_before_result_1[junkencount]))
    print("前々回のじゃんけん：" + junken_num_conv(junkendata_before_result_2[junkencount]) + str(junkendata_before_result_2[junkencount]))

    # 数値変換したデータをcsvファイルへ書き込み
    with open('Hikakin_Junken_Data.csv', 'a') as write_file:
        writer = csv.writer(write_file)
        writer.writerow([junkendata_result[junkencount], 
                        junkendata_month[junkencount], 
                        junkendata_nthweek[junkencount],
                        junkendata_before_result_1[junkencount], 
                        junkendata_before_result_2[junkencount]])


cursor.close()
con.close()