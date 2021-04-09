# coding:utf-8
from data.data_parse_write2 import data_parse_write2
from train.junken_train_operation2 import junken_train_operation2

if __name__ == "__main__":
    # じゃんけん予測のためのcsvデータを用意
    data_parse_write2()
    # csvデータから本日のじゃんけんを予測し、Mysqlに登録
    junken_train_operation2()