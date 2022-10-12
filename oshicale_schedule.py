# -*- coding:utf-8 -*-

import schedule
from time import sleep
import oshicale_account1

#定期動作させるタスクを設定
def tasks():
    oshicale_account1.main()

#30分おきの動作を設定
schedule.every(30).minutes.do(tasks)

#繰り返し実行させる。
while True:
    schedule.run_pending()
    sleep(1)
