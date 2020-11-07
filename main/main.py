# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:32
# @Author  : MA Ziqing
# @FileName: main.py

import sys
import time
import gflags
import logging
import schedule
from datetime import datetime
from sqlbase.create_sql_table import DbRandomCreator
from server.server import Server
from src.read_db_config import read_db_config

flags = gflags.FLAGS
gflags.DEFINE_integer('server_time_interval', 5, 'time interval of server run, default=?s')

logging.basicConfig(filename='main.log', level=logging.DEBUG)


def create_simulated_dataset():
    db_random_creator = DbRandomCreator()
    db_random_creator.create_all_table_randomly(
        time_interval_second=900,
        time_range=100)


def server_run():

    print('new turn server run')
    logging.info('[{}] server run, every {} seconds'.format(
        datetime.now(), flags.server_time_interval))
    server = Server()
    server.run_simulation()


def server_ph_run():
    config_dict = None
    try:
        config_dict = read_db_config()
    except Exception:
        print('请将 config.text 文件和 main.exe 放在同一文件夹下')
    if config_dict:
        print('new turn server_ph_run')
        server = Server(config_dict)
        server.ph_optimizer_run()


def trainer_run():
    pass


def job_example():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')
    print(flags.time)


def run_simulation(argv):
    flags(argv)
    logging.info('[{}] main start, run simulation'.format(datetime.now()))
    create_simulated_dataset()
    schedule.every(flags.server_time_interval).seconds.do(server_run)
    schedule.every().day.at('01:00').do(trainer_run)
    while True:
        schedule.run_pending()


def run_real(argv):
    try:
        config_dict = read_db_config()
    except Exception:
        print('请将 config.text 文件和 main.exe 放在同一文件夹下')

    flags(argv)
    schedule.every(flags.server_time_interval).seconds.do(server_ph_run)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    try:
        config_dict = read_db_config()
    # run_simulation(sys.argv)
    # run_real(sys.argv)
        print(config_dict)
    except:
        pass
    time.sleep(30)
