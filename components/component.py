# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 10:15
# @Author  : MA Ziqing
# @FileName: component.py.py
import random
from sqlbase.sql_pandas_cli import device_dict


class AlkaliInjector(object):
    def __init__(self):
        # self._cur_value_a = -1
        # self._cur_value_b = -1
        # self._change = -1
        self._drug_pred = 0
        self._return_result_a = {'id': -1,
                                 'turns': -1,
                                 'time': '',
                                 'device': device_dict['alkali_injector_frequency_a']['write_name'],
                                 'parameter': device_dict['alkali_injector_frequency_a']['chinese_name'],
                                 'originalValue': 10,
                                 'newValue': -1,
                                 'change': 0,
                                 'state': 1,
                                 'type': 2}
        self._return_result_b = {'id': -1,
                                 'turns': -1,
                                 'time': '',
                                 'device': device_dict['alkali_injector_frequency_b']['write_name'],
                                 'parameter': device_dict['alkali_injector_frequency_b']['chinese_name'],
                                 'originalValue': 10,
                                 'newValue': -1,
                                 'change': 0,
                                 'state': 1,
                                 'type': 2}

    def set_new_value(self, new_value_a, new_value_b):
        self._return_result_a['newValue'] = new_value_a
        self._return_result_b['newValue'] = new_value_b

    def get_new_value(self):
        return self._return_result_a['newValue'], self._return_result_b['newValue']

    def update_current_value(self, cli):
        value_a, value_b = cli.get_alkali_injector_data()
        self._return_result_a['originalValue'] = value_a
        self._return_result_b['originalValue'] = value_b
        return 0

    def get_current_value(self):
        return self._return_result_a['originalValue'], self._return_result_b['originalValue']

    def generate_result_randomly(self):
        new_value_delta = random.randint(-4, 4)
        self._return_result_a['newValue'] = self._return_result_a['originalValue'] + new_value_delta
        self._return_result_b['newValue'] = self._return_result_b['originalValue'] + new_value_delta
        return 0

    def get_result_and_drug_predict(self):
        return [self._return_result_a, self._return_result_b], self._drug_pred

