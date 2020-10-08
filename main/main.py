# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:32
# @Author  : MA Ziqing
# @FileName: main.py

from datetime import datetime
import schedule
import time


def job():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


if __name__ == '__main__':
    schedule.every().day.at('17:49').do.job(job)
    while True:
        schedule.run_pending()
