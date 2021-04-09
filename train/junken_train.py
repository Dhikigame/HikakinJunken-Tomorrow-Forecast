#coding:utf-8
from sklearn import svm, metrics, preprocessing, model_selection
from mlxtend.plotting import plot_decision_regions
import pandas as pd
import csv
from junken_result import junken_result


rock = "グー"
paper = "パー"
scissors = "チョキ"

# データ読み込み
dr_junken_all = pd.read_csv('../data/Hikakin_Junken_Data.csv', header=None)
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
X_train, X_test, train_label, test_label = model_selection.train_test_split(X_std, z, test_size=0.3, random_state=0)

# 学習用のデータと結果を学習する
clf.result.fit(X_train, train_label)




# # 2019年のデータをテストデータとし、各週のじゃんけんの結果と勝敗を出力
# f = open('../data_test/Input_Junken_TestData.csv', 'r')
# testdata_read = csv.reader(f)
win = 0
lose = 0
draw = 0
for junkencount in range(1100, len(z)):
    month = a[junkencount]
    day = b[junkencount]
    day_sub = c[junkencount]
    before_result_1 = d[junkencount]
    before_result_2 = e[junkencount]
    hikakin_result = z[junkencount]

    test_data = [[month, day, day_sub, before_result_1, before_result_2]]
    hikakin_result_pre = clf.result.predict(test_data)
    winning_losing_result = junken_result(month, day, hikakin_result, test_data, hikakin_result_pre)

    if winning_losing_result == "勝ち":
        win = win + 1
    if winning_losing_result == "負け":
        lose = lose + 1
    if winning_losing_result == "あいこ":
        draw = draw + 1

    print("------------------------------")
    print("勝：" + str(win) + ", 負：" + str(lose) + ", あいこ：" + str(draw))
    win_per = win / (win + lose) * 100
    print("勝率：" + str(win_per))



# 正答率を求める
pre = clf.result.predict(X_test)
ac_score = metrics.accuracy_score(test_label, pre)
print("正答率：", ac_score)
scores = model_selection.cross_val_score(clf.result, X_std, z, cv=10)
print("平均正解率 = ", scores.mean())
print("正解率の標準偏差 = ", scores.std())