# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 0:26
# @Author  : MA Ziqing

import os
import json
import logging
import random
import json
from datetime import datetime
from sqlbase.sql_pandas_cli import DataBasePandasClient
# from sqlbase.sql_cli import DataBaseSqlClient
from src.pre_treat_pandas import PreTreatPandas
# from optimizer.pid_optimizer import PidOptimizer
from src.constants import flags


class Monitor(object):
    def __init__(self, config_dict=None):
        self._name_ = 'monitor'
        if flags.version == 0:
            try:
                self._db_pandas_cli = DataBasePandasClient(config_dict)
                config_dict['dbname'] = 'YZSC'
                self._db_pandas_cli_write = DataBasePandasClient(config_dict)
                # self._db_sql_cli = DataBaseSqlClient(config_dict)
                # self._db_pandas_cli.get_db_data_test()
                print('【{}】【{}】 数据库连接正常 Monitor 以版本{}启动'.format(datetime.now(), self._name_, flags.version))
            except Exception as e:
                flags.version = 1
                print('【{}】【{}】 数据库连接无法建立，启动模拟版本，Monitor 以版本{}启动，错误原因：{}'.format(
                    datetime.now(), self._name_, flags.version, repr(e)))
        else:
            print('【{}】【{}】 数据库连接无法建立，启动模拟版本，Monitor 以版本{}启动'.format(datetime.now(), self._name_, flags.version))
        # self._pre_treat_pandas = PreTreatPandas()
        # self._pid_optimizer = PidOptimizer()

    def run(self):
        # df = self._db_pandas_cli.get_result1_last_two_row()
        turns = self._db_pandas_cli_write.get_last_turns_in_result1()
        # state = self._db_pandas_cli_write.get
        # for index in df.index:
        #     # 节电算法
        #     if df['type'][index] == 1:
        #         result2_device_list = []
        #         json_as_dict = json.loads(df['json'][index])
        #         device_json_list = json_as_dict['deviceList']
        #         for device_json in device_json_list:
        #             device = device_json['device']
        #             new_value = device_json['newValue']
        #             change, now_value = self.query_device_status(device, new_value)
        #             result2_device_list += [{'change': change,
        #                                      'device': device,
        #                                      'parameter': device_json['parameter'],
        #                                      'nowValue': now_value}]
        #         energy_saved = random.random.randint(0, 5)
        energy_past_24_hour = self._db_pandas_cli.get_electricity_past_x_hour(24)
        energy_past_48_hour = self._db_pandas_cli.get_electricity_past_x_hour(48)
        result2_dict = {'resultId': [0],
                        'turns': [turns],
                        'time': [datetime.now()],
                        'energyOriginal': [energy_past_48_hour - energy_past_24_hour],
                        'energyPred': [96],
                        'energyNow': [energy_past_24_hour],
                        'energySavedPred': [4],
                        'energySavedNow': [energy_past_48_hour - energy_past_24_hour * 2],
                        'drugOriginal': [100],
                        'drugPred': [96],
                        'drugNow': [95],
                        'drugSavedPred': [4],
                        'drugSavedNow': [5],
                        'state': [1],
                        'failReason': [0],
                        'type': ['1-2']
                        }
        print('【{}】【{}】 type=1, 优化结果为：{}'.format(datetime.now(), self._name_, result2_dict))
        self._db_pandas_cli_write.write_one_row_into_output_result2(result2_dict)

            # elif df['type'][index] == 2:
            #     result2_device_list = []
            #     json_as_dict = json.loads(df['json'][index])
            #     device_json_list = json_as_dict['deviceList']
            #     for device_json in device_json_list:
            #         device = device_json['device']
            #         new_value = device_json['newValue']
            #         change, now_value = self.query_device_status(device, new_value)
            #         result2_device_list += [{'change': change,
            #                                  'device': device,
            #                                  'parameter': device_json['parameter'],
            #                                  'nowValue': now_value}]
            #     drug_saved = random.randint(0, 6)
            #     result2_dict = {'resultId': [0],
            #                     'json': [json.dumps({'time': str(datetime.now()),
            #                                          'energyPred': -1,
            #                                          'energyNow': -1,
            #                                          'drugPred': self.query_total_drug_energy() - drug_saved,
            #                                          'drugNow': self.query_total_drug_energy(),
            #                                          'deviceList': result2_device_list})],
            #                     'state': [1],
            #                     'stype': [2]}
            #     print('【{}】【{}】 type=2, 优化结果为：{}'.format(datetime.now(), self._name_, result2_dict))
            #     self._db_pandas_cli.write_one_row_into_output_result2(result2_dict)

    def query_total_electronic_energy(self):
        return 100.0

    def query_total_drug_energy(self):
        # self._db_pandas_cli.
        return 100.0

    def query_device_status(self, device, new_value):
        return 0, random.randint(5, 10)


if __name__ == '__main__':
    pass