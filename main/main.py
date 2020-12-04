# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:32
# @Author  : MA Ziqing
# @FileName: main.py

import time
import logging
import schedule
import sys
import pymssql
from src.constants import flags
from datetime import datetime
# from sqlbase.create_sql_table import DbRandomCreator
from server.server import Server
from monitor.monitor import Monitor
from sqlbase.read_db_config import read_db_config

version = pymssql.get_dbversion()
logging.basicConfig(filename='main.log', level=logging.DEBUG)


# def create_simulated_dataset():
#     db_random_creator = DbRandomCreator()
#     db_random_creator.create_all_table_randomly(
#         time_interval_second=900,
#         time_range=100)


def run_all():
    _name_ = 'main'
    print('\n【{}】【{}】 新一轮调度开始 at version {}'.format(datetime.now(), _name_, flags.version))
    config_dict = None
    try:
        config_dict = read_db_config()
        print('【{}】【{}】 读取 config.text 文件成功'.format(datetime.now(), _name_))
        flags.version = 0
        flags.server_time_interval = config_dict['schedule_timestep_seconds']
    except Exception as e:
        print('【{}】【{}】 读取 config.txt 文件失败，原因：{}'.format(datetime.now(), _name_, repr(e)))
        flags.version = 1

    monitor = Monitor(config_dict)
    if flags.version == 0:
        monitor.run()
    server = Server(config_dict)
    server.run_real()
    a = 1


def run_real(argv):
    flags(argv)
    print('flags parsed')
    run_all()
    # schedule.every(flags.server_time_interval).seconds.do(run_all)
    # while True:
    #     schedule.run_pending()
    #     print('sleep 1: 10 seconds')
    #     time.sleep(10)


if __name__ == '__main__':
    run_real(sys.argv)
    print('sleep 2: 10 seconds')
    time.sleep(10)
