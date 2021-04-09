import csv


rock = "グー"       # グー
paper = "パー"      # パー
scissors = "チョキ" # チョキ

# じゃんけんの結果を文字列に変換
def junken_num_string(result):
    if result == 0:
        return rock
    if result == 1:
        return paper
    if result == 2:
        return scissors

# じゃんけんの手を勝つ手に変換
def junken_machine_learning(result):
    if result == "グー":
        return "パー"
    if result == "パー":
        return "チョキ"
    if result == "チョキ":
        return "グー"

def winning_losing(sazae_result, machine_learning_result):
    if sazae_result == "グー" and machine_learning_result == "グー":
        return "あいこ"
    if sazae_result == "グー" and machine_learning_result == "パー":
        return "勝ち"
    if sazae_result == "グー" and machine_learning_result == "チョキ":
        return "負け"

    if sazae_result == "パー" and machine_learning_result == "パー":
        return "あいこ"
    if sazae_result == "パー" and machine_learning_result == "チョキ":
        return "勝ち"
    if sazae_result == "パー" and machine_learning_result == "グー":
        return "負け"

    if sazae_result == "チョキ" and machine_learning_result == "チョキ":
        return "あいこ"
    if sazae_result == "チョキ" and machine_learning_result == "グー":
        return "勝ち"
    if sazae_result == "チョキ" and machine_learning_result == "パー":
        return "負け"


def junken_result(month, day, result_num, test_data, result_pre_num):
    # print(sazae_result)
    result_pre = junken_num_string(result_pre_num)
    machine_learning_result = junken_machine_learning(result_pre)
    hikakin_result = junken_num_string(int(result_num))

    winning_losing_result = winning_losing(hikakin_result, machine_learning_result)

    print("【" + str(month) + "月 " + str(day) + "日】")
    print("テストデータ：" + str(test_data) + ", ヒカキンさんの手予測：" + str(result_pre))
    print("機械学習の手：", machine_learning_result)
    print("ヒカキンさんの手：", hikakin_result)
    print("勝敗：", winning_losing_result)
    print()

    # writer = open('TestData_Result.csv', 'a')

    return winning_losing_result


# じゃんけんの予測結果と機械学習側の手で勝負
# def junken_result(month, nth_week, sazae_result_num, test_data, result_pre_num):
#     # print(sazae_result)
#     sazae_result_pre = junken_num_string(result_pre_num)
#     machine_learning_result = junken_machine_learning(sazae_result_pre)
#     sazae_result = junken_num_string(int(sazae_result_num))

#     winning_losing_result = winning_losing(sazae_result, machine_learning_result)

#     print("【2019年" + month + "月 第" + nth_week + "週】")
#     print("テストデータ：" + str(test_data) + ", サザエさんの手予測：" + str(sazae_result_pre))
#     print("機械学習の手：", machine_learning_result)
#     print("サザエさんの手：", sazae_result)
#     print("勝敗：", winning_losing_result)
#     print()

#     writer = open('TestData_Result.csv', 'a')

#     return winning_losing_result