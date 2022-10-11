#!/usr/bin/zsh

nohup /usr/bin/python 絶対パス/oshicale_schedule.py &!
#バックグラウンドにて実行させる

#OSHICALEシステムを動作させるときはこのシェルスクリプトを動作させてください。

#止めるときはps -xコマンドで出てきたoshicale_schedule.pyのプロセス番号をkill [プロセス番号]してください。
