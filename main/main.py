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
from sqlbase.read_db_config import read_db_config

version = pymssql.get_dbversion()
logging.basicConfig(filename='main.log', level=logging.DEBUG)


# def create_simulated_dataset():
#     db_random_creator = DbRandomCreator()
#     db_random_creator.create_all_table_randomly(
#         time_interval_second=900,
#         time_range=100)


def run_all():
    print('\n【{}】 新一轮调度开始 server_deoxidant_run scheduled at version {}'.format(datetime.now(), flags.version))
    config_dict = None
    try:
        config_dict = read_db_config()
        print('【{}】 读取 config.text 文件成功'.format(datetime.now()))
        flags.version = 0
        flags.server_time_interval = config_dict['schedule_timestep_minute']
    except Exception:
        print('【{}】 读取 config.txt 文件失败，请将 config.text 文件和 main.exe 放在同一文件夹下'.format(datetime.now()))
        flags.version = 1

    server = Server(config_dict)
    server.run_real()


def run_real(argv):
    flags(argv)
    schedule.every(flags.server_time_interval * 60).seconds.do(run_all)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    run_real(sys.argv)
    time.sleep(10)
