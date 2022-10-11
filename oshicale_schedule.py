# -*- coding:utf-8 -*-

import schedule
from time import sleep
import oshicale_account1

def tasks():
    oshicale_account1.main()

schedule.every(30).minutes.do(tasks)

while True:
    schedule.run_pending()
    sleep(1)
