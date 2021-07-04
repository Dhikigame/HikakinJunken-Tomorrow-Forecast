# coding:utf-8
from data.data_parse_write5 import data_parse_write5
from train.junken_train_operation5 import junken_train_operation5

if __name__ == "__main__":
    # じゃんけん予測のためのcsvデータを用意
    data_parse_write5()
    # csvデータから本日のじゃんけんを予測し、Mysqlに登録
    junken_train_operation5()