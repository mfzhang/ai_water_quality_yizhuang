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
from optimizer.pid_optimizer import PidOptimizer
from src.constants import flags

# logging.basicConfig(filename='server.log', level=logging.DEBUG)


class Server(object):
    def __init__(self, config_dict=None):
        self._name_ = 'server'
        if flags.version == 0:
            try:
                self._db_pandas_cli = DataBasePandasClient(config_dict)
                # self._db_sql_cli = DataBaseSqlClient(config_dict)
                self._db_pandas_cli.get_db_data_test()
                print('【{}】【{}】数据库连接正常 Server 以版本{}启动'.format(datetime.now(), self._name_, flags.version))
            except Exception as e:
                flags.version = 1
                print('【{}】【{}】 数据库连接无法建立，启动模拟版本，Server 以版本{}启动，错误原因：{}'.format(
                    datetime.now(), self._name_, flags.version, repr(e)))
        else:
            print('【{}】【{}】 数据库连接无法建立，启动模拟版本，Server 以版本{}启动'.format(datetime.now(), self._name_, flags.version))
        self._pre_treat_pandas = PreTreatPandas()
        self._pid_optimizer = PidOptimizer()

    def ph_optimizer_run(self):
        # pH 优化模块：利用负反馈调节使出水 pH 在 6.5 附近变动
        if flags.version == 0:
            df_ph = self._db_pandas_cli.get_ph_monitor_data_to_df()
            a = 1
            # df_ph = self._pre_treat_pandas.mask_extreme_value(df_ph)
            # df_pump = None
            result, drug_pred = self._pid_optimizer.optimize_ph_with_pid(df_ph=None, df_pump=None)
        elif flags.version == 1:
            # print('server start with version 1')
            result, drug_pred = self._pid_optimizer.optimize_ph_with_pid(df_ph=None, df_pump=None)
        else:
            # print('server version false', flags.version)
            drug_pred = None
            result = None
        print('【{}】【{}】 schedule result: {} '.format(datetime.now(), self._name_, result))
        return result, drug_pred

    # def qmf_optimizer_run(self):
    #     # quantity_micro_filter 微滤进水流量优化模块：使进水与出水相当
    #     df_outflow = self._db_pandas_cli.get_outflow_quantity_data()
    #     df_outflow = self._pre_treat_pandas.mask_extreme_value(df_outflow)
    #     result = self._pid_optimizer.optimizer_mf_by_outflow_with_pid(df_outflow)
    #     return result

    def deoxidant_optimizer_run(self):
        result, drug_pred = self._pid_optimizer.optimze_deoxidant_by_orp_with_pid()
        print('【{}】【{}】 schedule result: {} '.format(datetime.now(), self._name_, result))
        return result, drug_pred

    def ro_number_optimizer_run(self):
        result, energy_pred = self._pid_optimizer.optimizer_mf_by_outflow_with_pid()
        print('【{}】【{}】 schedule result: {} '.format(datetime.now(), self._name_, result))
        return result, energy_pred

    def write_result(self, result_list, resource_pred_list, optimize_type=1):
        logging.info('【{}】【{}】 write result 【{}】 into OutputDB'.format(
            datetime.now(), self._name_, result_list
            ))
        if optimize_type == 1:
            row_json = {
                'time': str(datetime.now()),
                'energyPred': resource_pred_list[0],
                'drugPred': 0,
                'deviceList': result_list}
        else:
            row_json = {
                'time': str(datetime.now()),
                'energyPred': 0,
                'drugPred': resource_pred_list[0],
                'deviceList': result_list}
        rows = {'id': [1],
                # 'json': [json.dumps(row_json)],
                'json': ['111'],
                'state': [1],
                'type': [optimize_type]
                }
        # self._db_sql_cli = DataBaseSqlClient()
        print('【{}】【{}】 type={}, 优化结果为：{}'.format(datetime.now(), self._name_, optimize_type, row_json))
        if flags.version == 0:

            print('【{}】【{}】 调度结果写入数据库'.format(datetime.now(), self._name_))
            self._db_pandas_cli.write_one_row_into_output_result1(rows)
        else:
            print('【{}】【{}】 数据库无法连接，调度结果只做展示，无法写入数据库'.format(datetime.now(), self._name_))

    def run_real(self):
        result_list_energy = []
        result_list_drug = []
        energy_saved = 0
        drug_saved = 0

        json_res_ph, drug_pred = self.ph_optimizer_run()
        if json_res_ph:
            result_list_drug += [json_res_ph]
            drug_saved += drug_pred

        json_res_deoxidant, drug_pred = self.deoxidant_optimizer_run()
        if json_res_deoxidant:
            result_list_drug += [json_res_deoxidant]
            drug_saved += drug_pred

        json_res_ro_number, drug_pred = self.ro_number_optimizer_run()
        if json_res_ro_number:
            result_list_energy += [json_res_ro_number]
            energy_saved += energy_saved

        # 写入节电算法结果
        self.write_result(result_list_energy, [energy_saved, drug_saved], optimize_type=1)
        # 写入节药算法结果
        self.write_result(result_list_drug, [energy_saved, drug_saved], optimize_type=2)


def test():
    logging.info('[{}] Server start'.format(datetime.now()))
    server = Server()
    server.run_real()


if __name__ == '__main__':
    test()
