# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 0:26
# @Author  : MA Ziqing

import os
import json
import logging
import json
from datetime import datetime
from sqlbase.sql_pandas_cli import DataBasePandasClient
# from sqlbase.sql_cli import DataBaseSqlClient
from src.pre_treat_pandas import PreTreatPandas
from optimizer.pid_optimizer import PidOptimizer
from src.constants import flags


class Monitor(object):
    def __init__(self, config_dict=None):
        if flags.version == 0:
            try:
                self._db_pandas_cli = DataBasePandasClient(config_dict)
                # self._db_sql_cli = DataBaseSqlClient(config_dict)
                self._db_pandas_cli.get_db_data_test()
                print('【{}】 数据库连接正常 Monitor 以版本{}启动'.format(datetime.now(), flags.version))
            except Exception as e:
                flags.version = 1
                print('【{}】 数据库连接无法建立，启动模拟版本，Monitor 以版本{}启动，错误原因：{}'.format(
                    datetime.now(), flags.version, repr(e)))
        else:
            print('【{}】 数据库连接无法建立，启动模拟版本，Monitor 以版本{}启动'.format(datetime.now(), flags.version))
        # self._pre_treat_pandas = PreTreatPandas()
        # self._pid_optimizer = PidOptimizer()

    def run(self):
        df = self._db_pandas_cli.get_result1_last_two_row()
        for index in df.index:
            # 节点算法
            if df['type'][index] == 1:
                result2_device_list = []
                json_as_dict = json.loads(df['json'])
                device_json_list = json_as_dict['deviceList']
                for device_json in device_json_list:
                    device = device_json['device']
                    new_value = device_json['newValue']
                    change, now_value = self.query_device_status(device, new_value)
                    result2_device_list += [{'change':change,
                                           'device': device,
                                           'parameter': device_json['parameter'],
                                           'nowValue': now_value}]
                result2 = {'id': 0,
                           'time': str(datetime.now()),
                           'energyPred': 10.2,
                           'energyNow': 12,
                           'drugPred': 11,
                           'drugNow': 5,
                           'deviceList': result2_device_list,
                           'state': 1,
                           'type': 1}
                self._db_pandas_cli.write_one_row_into_output_result2(result2)

            elif df['type'][index] == 2:
                result2_device_list = []
                json_as_dict = json.loads(df['json'])
                device_json_list = json_as_dict['deviceList']
                for device_json in device_json_list:
                    device = device_json['device']
                    new_value = device_json['newValue']
                    change, now_value = self.query_device_status(device, new_value)
                    result2_device_list += [{'change':change,
                                           'device': device,
                                           'parameter': device_json['parameter'],
                                           'nowValue': now_value}]
                result2 = {'id': 0,
                           'time': str(datetime.now()),
                           'energyPred': 10.2,
                           'energyNow': 12,
                           'drugPred': 11,
                           'drugNow': 5,
                           'deviceList': result2_device_list,
                           'state': 1,
                           'type': 1}
                self._db_pandas_cli.write_one_row_into_output_result2(result2)

    def query_device_status(self, device, new_value):
        return 0, 5