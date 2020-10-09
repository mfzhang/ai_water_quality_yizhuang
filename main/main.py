# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:32
# @Author  : MA Ziqing
# @FileName: main.py

import schedule
import time
import gflags
import logging
from datetime import datetime
from sqlbase.create_sql_table import DbRandomCreator

flags = gflags.FLAGS
gflags.DEFINE_integer('time', 15, 'time')

logging.basicConfig(filename='main.log', level=logging.DEBUG)


def create_simulated_dataset():
    db_random_creator = DbRandomCreator()
    db_random_creator.create_all_table_randomly(
        time_interval_second=900,
        time_range=100)


def job():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')
    print(flags.time)


if __name__ == '__main__':
    logging.info('[{}] main start'.format(datetime.now()))
    create_simulated_dataset()
    # schedule.every().day.at('17:49').do.job(job)
    # while True:
    #     schedule.run_pending()
