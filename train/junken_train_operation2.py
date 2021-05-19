# coding:utf-8
import io,sys
from sklearn import svm, metrics, preprocessing, model_selection
from mlxtend.plotting import plot_decision_regions
import pandas as pd
import csv
import platform
import os
import MySQLdb
from datetime import datetime
from datetime import date
from train.junken_result import junken_result
sys.path.append('..')
from info.information import Information


def junken_train_operation2():
    # Unicodeからutf-8へ変換
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os_system = platform.system()
    if "Darwin" in os_system:
        # データ読み込み
        dr_junken_all = pd.read_csv(Information.csv_dir("Darwin"), header=None)
    else:
        # データ読み込み
        dr_junken_all = pd.read_csv(Information.csv_dir("Linux"), header=None)
    dr_junken = dr_junken_all[[0,1,2,3,4,5]]
    dr_junken.columns = [u'result', u'month', u'day', u'day_sub', u'before_result_1', u'before_result_2']
    pd.DataFrame(dr_junken)

    # 説明変数
    a = dr_junken["month"]
    b = dr_junken["day"]
    c = dr_junken["day_sub"]
    d = dr_junken["before_result_1"]
    e = dr_junken["before_result_2"]
    # 目的変数
    z = dr_junken["result"]

    # SVMの中からLinearSVCを使用するための準備
    X = dr_junken[['month', 'day', 'day_sub', 'before_result_1', 'before_result_2']]
    sc = preprocessing.StandardScaler()
    sc.fit(X)
    X_std = sc.transform(X)
    clf = svm.LinearSVC()

    # モデル作成
    clf.result = svm.SVC(C=1.0, kernel='poly', degree=3)

    # データ分割(テストデータ3割、残りは教師データ)
    X_train, X_test, train_label, test_label = model_selection.train_test_split(X_std, z, test_size=0.1)

    # 学習用のデータと結果を学習する
    clf.result.fit(X_train, train_label)


    win = 0
    lose = 0
    draw = 0
    win_per = 0
    # 前回の日付を取得
    before_month : int = a[len(z)-1]
    before_day : int = b[len(z)-1]
    before_result_1 : int = z[len(z)-1]
    before_result_2 : int = d[len(z)-1]
    # 今日の日付を取得
    dt_now = datetime.now()
    now_year : int = dt_now.year
    now_month : int = dt_now.month
    now_day : int = dt_now.day
    before_year : int = before_year_calc(before_month, now_month, now_year)
    # print("前回の年：" + str(before_year))
    # print("前回の月：" + str(before_month))
    # print("前回の日：" + str(before_day))
    # print("前回の結果：" + str(before_result_1))
    # print("前々回の結果：" + str(before_result_2))
    # print()
    # print("今日の年：" + str(now_year))
    # print("今日の月：" + str(now_month))
    # print("今日の日：" + str(now_day))
    # print()
    day_sub = before_now_day_sub(before_year, before_month, before_day, now_year, now_month, now_day)
    # print("今日と前回の日付差分：" + str(day_sub))
    # print()
    predict_data = [[now_month, now_day, day_sub, before_result_1, before_result_2]]
    hikakin_result_pre = clf.result.predict(predict_data)
    result_predict = hikakin_result_pre[0]
    # print("今日のじゃんけん予測：" + str(result_predict))

    # for junkencount in range(0, len(z)):
    #     month = a[junkencount]
    #     day = b[junkencount]
    #     day_sub = c[junkencount]
    #     before_result_1 = d[junkencount]
    #     before_result_2 = e[junkencount]
    #     hikakin_result = z[junkencount]

    #     test_data = [[month, day, day_sub, before_result_1, before_result_2]]
    #     hikakin_result_pre = clf.result.predict(test_data)
    #     winning_losing_result = junken_result(month, day, hikakin_result, test_data, hikakin_result_pre)

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
