# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 10:15
# @Author  : MA Ziqing
# @FileName: component.py.py
import random
from sqlbase.sql_pandas_cli import device_dict, DataBasePandasClient
from src.constants import PhStandard
from components.paramter import ParameterBase


class DeviceBase(object):
    def __int__(self):
        self.device_list = []

    def __iter__(self):
        return (i for i in self.device_list)

    def __repr__(self):
        return str([i for i in self.device_list])

    # def add_device(self, device_list):
    #     self.device_list = [ParameterBase(i) for i in device_list]

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
            if average_ph > PhStandard.MAXLIMIT:
                self.set_new_value(a - delta, b - delta)
            elif average_ph < PhStandard.MINLIMIT:
                self.set_new_value(a + delta, b + delta)
            else:
                self.set_new_value(a, b)
        else:
            self.set_new_value(a, b)
        # result = self.get_return_result_list()


class DeoxidantInjector(DeviceBase):
    def __init__(self):
        device_list = ['deoxidant_injector_frequency_c', 'deoxidant_injector_frequency_d']
        self.device_list = tuple(ParameterBase(i) for i in device_list)

    def optimize_pid(self):
        value_tuple = self.get_current_value()
        new_value_tuple = ()
        for i in value_tuple:
            if i > 1:
                new_value_tuple += (i * (100 + random.randint(-5, 5)) / 100,)
            else:
                new_value_tuple += (i,)
        self.set_new_value(*new_value_tuple)


class MicroFiltrationInjector(DeviceBase):
    def __init__(self):
        name_list = ['a', 'b', 'c', 'd', 'e', 'f']
        device_list = ['mf_inflow_{}'.format(i) for i in name_list]
        self.device_list = tuple(ParameterBase(i) for i in device_list)

    def optimize_pid(self):
        value_tuple = self.get_current_value()
        new_value_tuple = ()
        for i in value_tuple:
            if i > 1:
                new_value_tuple += (i * (100 + random.randint(-5, 5)) / 100,)
            else:
                new_value_tuple += (i,)
        self.set_new_value(*new_value_tuple)


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
