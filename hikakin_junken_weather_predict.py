# coding:utf-8
from data.data_parse_write4 import data_parse_write4
from train.junken_train_operation4 import junken_train_operation4
from tools.junken_random import junken_random

if __name__ == "__main__":
    # # じゃんけん予測のためのcsvデータを用意
    # data_parse_write4()
    # # csvデータから本日のじゃんけんを予測し、Mysqlに登録
    # junken_train_operation4()

    # じゃんけんをランダムで予測し、Mysqlに登録
    junken_random()