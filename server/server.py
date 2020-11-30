# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:26
# @Author  : MA Ziqing
# @FileName: server.py.py
import os
import json
import logging
from datetime import datetime
from sqlbase.sql_pandas_cli import DataBasePandasClient
# from sqlbase.sql_cli import DataBaseSqlClient
from src.pre_treat_pandas import PreTreatPandas
# from optimizer.pid_optimizer import PidOptimizer
from src.constants import flags
from components.component import *

# logging.basicConfig(filename='server.log', level=logging.DEBUG)


def decorator_server_run(func1):
    def func2(*args):
        result, pred = func1(*args)
        print('【{}】【{}】 schedule result: {} '.format(datetime.now(), func1.__name__, result))
        return result, pred
    return func2


class Server(object):
    def __init__(self, config_dict=None):
        self._name_ = 'server'
        if flags.version == 0:
            try:
                config_dict['dbname'] = 'Runtime'
                self._db_pandas_cli = DataBasePandasClient(config_dict)
                config_dict['dbname'] = 'YZSC'
                self._db_pandas_cli_write = DataBasePandasClient(config_dict)
                # self._db_sql_cli = DataBaseSqlClient(config_dict)
                # self._db_pandas_cli.get_db_data_test()
                print('【{}】【{}】数据库连接正常 Server 以版本{}启动'.format(datetime.now(), self._name_, flags.version))
            except Exception as e:
                flags.version = 1
                print('【{}】【{}】 数据库连接无法建立，启动模拟版本，Server 以版本{}启动，错误原因：{}'.format(
                    datetime.now(), self._name_, flags.version, repr(e)))
        else:
            print('【{}】【{}】 数据库连接无法建立，启动模拟版本，Server 以版本{}启动'.format(datetime.now(), self._name_, flags.version))
        self._pre_treat_pandas = PreTreatPandas()

    @decorator_server_run
    def ph_optimizer_run(self):
        # pH 优化模块：利用负反馈调节使出水 pH 在 6.5 附近变动
        alkali_injector = AlkaliInjector()
        df_ph = self._db_pandas_cli.get_ph_monitor_data_to_df()
        alkali_injector.update_current_value(cli=self._db_pandas_cli)
        alkali_injector.optimize_pid(df_ph)
        result = alkali_injector.get_return_result_list()
        drug_pred = 0
        return result, drug_pred

    @decorator_server_run
    def deoxidant_optimizer_run(self):
        deoxidant_injector = DeoxidantInjector()
        deoxidant_injector.update_current_value(self._db_pandas_cli)
        deoxidant_injector.optimize_pid()
        result = deoxidant_injector.get_return_result_list()
        drug_pred = 0
        return result, drug_pred

    # def ro_number_optimizer_run(self):
    #     pass

    @decorator_server_run
    def mf_inflow_optimizer_run(self):
        mf_inflow = MicroFiltrationInjector()
        mf_inflow.update_current_value(self._db_pandas_cli)
        mf_inflow.optimize_pid()
        result = mf_inflow.get_return_result_list()
        energy_pred = 0
        return result, energy_pred

    def write_result(self, result_list):
        logging.info('【{}】【{}】 write result 【{}】 into OutputDB'.format(
            datetime.now(), self._name_, result_list
            ))
        turns = self._db_pandas_cli_write.get_last_turns_in_result1()
        if flags.version == 0:
            print('【{}】【{}】 调度结果写入数据库'.format(datetime.now(), self._name_))
            for row in result_list:
                row['time'] = datetime.now()
                row['turns'] = turns + 1
                self._db_pandas_cli_write.write_one_row_into_output_result1(row)
        else:
            print('【{}】【{}】 数据库无法连接，调度结果只做展示，无法写入数据库'.format(datetime.now(), self._name_))

    def run_real(self):
        result_list = []
        drug_saved = 0

        json_res_ph, drug_pred = self.ph_optimizer_run()
        result_list += json_res_ph
        drug_saved += drug_pred

        res_mf, energy_pred = self.mf_inflow_optimizer_run()
        result_list += res_mf

        res_deoxidant, drug_pred = self.deoxidant_optimizer_run()
        result_list += res_deoxidant

        # json_res_ro_number, drug_pred = self.ro_number_optimizer_run()
        # if json_res_ro_number:
        #     result_list += [json_res_ro_number]
        #     energy_saved += energy_saved

        # 写入节电节药算法结果
        self.write_result(result_list)


def test():
    logging.info('[{}] Server start'.format(datetime.now()))
    server = Server()
    server.run_real()


if __name__ == '__main__':
    test()
