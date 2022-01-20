# coding:utf-8
import io,sys
from sklearn import svm, metrics, preprocessing, model_selection
from mlxtend.plotting import plot_decision_regions
import pandas as pd
import csv
import platform
import calendar
import os
import MySQLdb
from datetime import datetime
from datetime import date
import random
# from train.junken_result import junken_result
from info.information import Information



def junken_random():
    # Unicodeからutf-8へ変換
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os_system = platform.system()
    # if "Darwin" in os_system:
    #     # データ読み込み
    #     dr_junken_all = pd.read_csv(Information.csv_dir("Darwin"), header=None)
    # else:
    #     # データ読み込み
    #     dr_junken_all = pd.read_csv(Information.csv_dir("Linux"), header=None)
    # dr_junken = dr_junken_all[[0,1,2,3,4,5]]
    # dr_junken.columns = [u'result', u'month', u'nth_week', u'before_result_1', u'before_result_2', u'before_result_3']
    # pd.DataFrame(dr_junken)

    # # 説明変数
    # a = dr_junken["month"]
    # b = dr_junken["nth_week"]
    # c = dr_junken["before_result_1"]
    # d = dr_junken["before_result_2"]
    # e = dr_junken["before_result_3"]
    # # 目的変数
    # z = dr_junken["result"]

    # # SVMの中からLinearSVCを使用するための準備
    # X = dr_junken[['month', 'nth_week', 'before_result_1', 'before_result_2', 'before_result_3']]
    # sc = preprocessing.StandardScaler()
    # sc.fit(X)
    # X_std = sc.transform(X)
    # clf = svm.LinearSVC()

    # # モデル作成
    # clf.result = svm.SVC(C=1.0, kernel='poly', degree=3)

    # # データ分割(テストデータ3割、残りは教師データ)
    # X_train, X_test, train_label, test_label = model_selection.train_test_split(X_std, z, test_size=0.3, random_state=0)

    # # 学習用のデータと結果を学習する
    # clf.result.fit(X_train, train_label)

    # # 前回の日付を取得
    # before_month : int = a[len(z)-1]
    # nth_week : int = b[len(z)-1]
    # before_result_1 : int = z[len(z)-1]
    # before_result_2 : int = c[len(z)-1]
    # before_result_3 : int = d[len(z)-1]
    # 今日の日付を取得
    dt_now = datetime.now()
    now_year : int = dt_now.year
    now_month : int = dt_now.month
    now_day : int = dt_now.day
    # now_nth_week : int = get_nth_week(now_year, now_month, now_day)
    print(dt_now)

    # predict_data = [[now_month, now_nth_week, before_result_1, before_result_2, before_result_3]]
    # hikakin_result_pre = clf.result.predict(predict_data)
    # result_predict = hikakin_result_pre[0]

    # win = 0
    # lose = 0
    # draw = 0
    # win_per = 0 
    # for junkencount in range(150, len(z)):
    #     month = a[junkencount]
    #     nth_week = b[junkencount]
    #     before_result_1 = c[junkencount]
    #     before_result_2 = d[junkencount]
    #     before_result_3 = e[junkencount]
    #     hikakin_result = z[junkencount]

    #     test_data = [[month, nth_week, before_result_1, before_result_2, before_result_3]]
    #     hikakin_result_pre = clf.result.predict(test_data)
    #     winning_losing_result = junken_result_nthweek(month, nth_week, hikakin_result, test_data, hikakin_result_pre)

    #     if winning_losing_result == "勝ち":
    #         win = win + 1
    #     if winning_losing_result == "負け":
    #         lose = lose + 1
    #     if winning_losing_result == "あいこ":
    #         draw = draw + 1

    #     print("------------------------------")
    #     print("勝：" + str(win) + ", 負：" + str(lose) + ", あいこ：" + str(draw))
    #     if win != 0 and lose != 0:
    #         win_per = win / (win + lose) * 100
    #     print("勝率：" + str(win_per))


    # 正答率を求める
    # pre = clf.result.predict(X_test)
    # ac_score = metrics.accuracy_score(test_label, pre)
    # print("正答率：", ac_score)
    # scores = model_selection.cross_val_score(clf.result, X_std, z, cv=10)
    # print("平均正解率 = ", scores.mean())
    # print("正解率の標準偏差 = ", scores.std())

    # 
    result_predict = random.randrange(3)
    # Mysqlに機械学習で得られた予測結果をを挿入・更新する
    os_system = platform.system()
    if "Darwin" in os_system:
        con = MySQLdb.connect(unix_socket=Information.db_socket("Darwin"),user=Information.db_user("Darwin"),passwd=Information.db_passwd("Darwin"),host=Information.db_host("Darwin"),db=Information.db_name("Darwin"),use_unicode=Information.use_unicode("Darwin"),charset=Information.charset("Darwin"))
    else:
        con = MySQLdb.connect(unix_socket=Information.db_socket("Linux"),user=Information.db_user("Linux"),passwd=Information.db_passwd("Linux"),host=Information.db_host("Linux"),db=Information.db_name("Linux"),use_unicode=Information.use_unicode("Linux"),charset=Information.charset("Linux"))
    cursor = con.cursor()

    # sql = 'select upload_date from hikakin_junken_weather where upload_date = "' + str(date(now_year, now_month, now_day)) + '" limit 1'
    # print(sql)
    # cursor.execute(sql)
    # get_uploaddate = cursor.fetchall()
    # latest_upload_date = date_conv(get_uploaddate[0])
    # print(str(latest_upload_date))
    # if str(latest_upload_date) != str(date(now_year, now_month, now_day)):
    sql = 'insert into hikakin_junken_weather(upload_date, weather_result) values("' + str(date(now_year, now_month, now_day)) + '", ' + str(result_predict) + ')'
    # print(sql)
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()



# 年月日が月の第何週か求める
def get_nth_week(year, month, day, firstweekday=6):
    # calendar.monthrange:指定された月の一日の曜日と日数を返す
    first_dow = calendar.monthrange(int(year), int(month))[0]
    offset = (first_dow - int(firstweekday)) % 7
    return (int(day) + offset - 1) // 7 + 1

def before_year_calc(before_month, now_month, now_year):
    if now_month == 1 and before_month == 12:
        before_year = now_year - 1
    else:
        before_year = now_year
    return before_year

def before_now_day_sub(before_year : int, before_month : int, before_day : int, now_year : int, now_month : int, now_day : int):
    before_date = date(before_year, before_month, before_day)
    now_date = date(now_year, now_month, now_day)
    return (now_date-before_date).days

def date_conv(date_):
    return datetime.strptime(str(date_), '%Y-%m-%d')
