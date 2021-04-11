# HikakinJunken-Tomorrow-Forecast

Youtuberヒカキンさんの投稿した動画で行われるジャンケンが格納されたDBから次の動画で行われるジャンケンを予測する機械学習プログラム

Youtuber HikakinTV Channel : https://www.youtube.com/channel/UCZf__ehlCEBPop-_sldpBUQ

A machine learning program that predicts rock-paper-scissors to be performed in the next video from the DB that stores rock-paper-scissors performed in the video posted by Youtuber Hikakin.

Youtuber HikakinTV Channel : https://www.youtube.com/channel/UCZf__ehlCEBPop-_sldpBUQ

# DEMO
以下のようなサイトに学習して予測した手を毎朝6時に公開しています

https://hikakinjunken.tk/

The hands that I learned and predicted on the following sites are published every morning at 6 o'clock

https://hikakinjunken.tk/


<img width="1146" alt="スクリーンショット 2021-04-11 午後2 28 04" src="https://user-images.githubusercontent.com/12876144/114293575-32bd2b80-9ad2-11eb-92f2-28266c17b82c.png">

# Features
- Mysqlに登録されているYoutubeで投稿したヒカキンさんの動画情報とそこで行われたジャンケン情報から機械学習のための教師データに変換する
- 教師データが保存されたcsvファイルからSVMを使用した教師あり学習でモデルを生成する
- モデルから次の動画で何の手を出すか予測した手をDBに更新する
<br>

- Convert Hikakin's video information posted on Youtube registered in Mysql and rock-paper-scissors information performed there to teacher data for machine learning
- Generate a model with supervised learning using SVM from a csv file that stores teacher data
- Update the hand that predicted what to do in the next video from the model to the DB

# Requirement
* Python3
* Mysql
* sklearn


# Author
* Dhiki(Infrastructure engineer & Video contributor)
* https://twitter.com/DHIKI_pico


# License
ご自由に使用いただいて構いません。

Feel free to use it.
