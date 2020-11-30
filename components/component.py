# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 10:15
# @Author  : MA Ziqing
# @FileName: component.py.py
import random
from sqlbase.sql_pandas_cli import device_dict, DataBasePandasClient
from src.constants import PhStandard


class ParameterBase(object):
    def __init__(self, parameter_name):
        self._paramter_name = parameter_name
        self._cur_value = -1
        self._new_value = -1
        self._return_res = {'id': -1,
                            'turns': -1,
                            'time': '',
                            'device': device_dict[parameter_name]['write_name'],
                            'parameter': device_dict[parameter_name]['chinese_name'],
                            'originalValue': -1,
                            'newValue': -1,
                            'change': 0,
                            'state': 1,
                            'type': -1}

    def __repr__(self):
        return '【{}】 cur_value: {}, new_value:{}'.format(self._paramter_name, self._cur_value, self._new_value)

    def set_cur_value(self, cur_value):
        self._cur_value = cur_value

    def get_cur_value(self):
        return self._cur_value

    def update_cur_value(self, cli):
        self._cur_value = cli.get_current_data_mean_of_1min_by_device_name(device_dict[self._paramter_name]['read_name'])

    def set_new_value(self, new_value):
        self._new_value = new_value

    def get_new_value(self):
        return self._new_value

    def get_return_result(self):
        self._return_res['originalValue'] = self.get_cur_value()
        self._return_res['newValue'] = self.get_new_value()
        return self._return_res


class DeviceBase(object):
    def __int__(self):
        self.device_list = []
        print('father class')
    # device_list = device_list

    def __iter__(self):
        return (i for i in self.device_list)

    def __repr__(self):
        return str([i for i in self.device_list])

    def add_device(self, device_list):
        self.device_list = [ParameterBase(i) for i in device_list]

    def set_new_value(self, *args):
        for i, j in zip(self.device_list, args):
            i.set_new_value(j)

    def get_new_value(self):
        return tuple(i.get_new_value() for i in self.device_list)

    def update_current_value(self, cli):
        for i in self.device_list:
            i.update_cur_value(cli)

    def get_current_value(self):
        return tuple(i.get_cur_value() for i in self.device_list)

    def get_return_result_list(self):
        return [i.get_return_result() for i in self.device_list]

    def optimize_pid(self):
        self.set_new_value(*self.get_current_value())


class AlkaliInjector(DeviceBase):
    def __init__(self):
        device_list = ['alkali_injector_frequency_a', 'alkali_injector_frequency_b']
        self.device_list = tuple(ParameterBase(i) for i in device_list)

    def optimize_pid(self, df_ph):
        a, b = self.get_current_value()
        average_ph = df_ph.mean()
        delta = 0.1
        if 1 < average_ph < 13:
            if df_ph.mean() > PhStandard.MAXLIMIT:
                self.set_new_value(a - delta, b - delta)
            elif df_ph.mean() < PhStandard.MINLIMIT:
                self.set_new_value(a + delta, b + delta)
            else:
                self.set_new_value(a, b)
        else:
            self.set_new_value(a, b)
        result = self.get_return_result_list()


class DeoxidantInjector(DeviceBase):
    def __init__(self):
        device_list = ['deoxidant_injector_frequency_c', 'deoxidant_injector_frequency_d']
        self.device_list = tuple(ParameterBase(i) for i in device_list)


class MicroFiltrationInjector(DeviceBase):
    def __init__(self):
        name_list = ['a', 'b', 'c', 'd', 'e', 'f']
        device_list = ['mf_inflow_{}'.format(i) for i in name_list]
        self.device_list = tuple(ParameterBase(i) for i in device_list)


# class MicroFiltrationInflow(DeviceBase):
#     def __int__(self):
#         name_list = ['a', 'b', 'c', 'd', 'e', 'f']
#         device_list = ['mf_inflow_{}'.format(i) for i in name_list]
#         self.device_list = tuple(ParameterBase(i) for i in device_list)


class Test(DeviceBase):
    def __int__(self):
        self.device_list = [1, 2, 3]


def test():
    config_dict = {"host": "84.20.85.106", "user": "sa", "password": "monitor@333",
                   "dbname": "Runtime", "schedule_timestep_seconds": 1}
    cli = DataBasePandasClient(config_dict=config_dict)
    alkali_injector = AlkaliInjector()
    deoxidant_injector = DeoxidantInjector()
    mf_inflow = MicroFiltrationInjector()
    mf_inflow.update_current_value(cli=cli)
    alkali_injector.update_current_value(cli=cli)
    deoxidant_injector.update_current_value(cli=cli)
    print(alkali_injector.get_new_value())
    print(alkali_injector.get_return_result_list())
    print(deoxidant_injector.get_return_result_list())


if __name__ == '__main__':
    test()
