# korokoro_keeper

## 概要

ボールが発射した角度とゴール位置から、学習を行い優秀なキーパーとなるプログラム。

## ファイル構成

### function_data.csv

学習した結果を格納するファイル。
具体的には、 "切片" と "傾き" を保存する。

### grovepi.py / grovepi.pyc

ラズベリーパイ上で動かすのに必要なファイル。

### watch_data.sh

各 CSV ファイルの中身を 約 2秒ごとに 出力するプログラム。

### main.py

メインプログラム。
このファイルを実行することにより、制御を行う。

## 実行の方法

1. 本リポジトリまで移動する。お借りしたラズベリーパイ上では、 "~/Desktop/Kawaguchisan/korokoro_keeper" に存在するので、以下のコマンドで行けるかなと。

`$ cd ~/Desktop/Kawaguchisan/korokoro_keeper"

2. 監視用 シェルスクリプト を実行する。

`$ sh watch_data.sh`

3. メインプログラムを実行する。（言わずもがなですが、ターミナル 2つ 開く必要性があります。）

`$ python main.py`
