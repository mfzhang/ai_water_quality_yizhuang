# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:26
# @Author  : MA Ziqing
# @FileName: server.py.py
import os
import logging
from datetime import datetime
from sqlbase.sql_pandas_cli import DataBasePandasClient
from sqlbase.sql_table_base import INDICATOR_LIST, INJECTOR_LIST
from src.pre_treat_pandas import PreTreatPandas
from optimizer.pid_optimizer import PidOptimizer

# logging.basicConfig(filename='server.log', level=logging.DEBUG)


class Server(object):
    def __init__(self):
        self._db_pandas_cli = DataBasePandasClient()
        self._pre_treat_pandas = PreTreatPandas()
        self._pid_optimizer = PidOptimizer()

    def get_input_data(self):
        table_name = INJECTOR_LIST[0].__tablename__
        return self._db_pandas_cli.get_quality_indicator_data(table_name)

    def get_label_data(self):
        table_name = INDICATOR_LIST[0].__tablename__
        return self._db_pandas_cli.get_quality_indicator_data(table_name)

    def pre_treat_input_data(self, df):
        return self._pre_treat_pandas.mask_extreme_value(df)

    def treat_with_ml_model(self, df):
        return df

    def optimize_config(self, df_out, df_out_pred):
        output_instruct = self._pid_optimizer.optimize_config_with_pid(df_out, df_out_pred)
        return output_instruct

    def run(self):
        counter_max = 5
        counter = 0
        while True:
            counter += 1
            if counter > counter_max:
                break
            df_inp = self.get_input_data()
            df_inp = self.pre_treat_input_data(df_inp)
            df_out_pred = self.treat_with_ml_model(df_inp)
            df_out = self.get_label_data()
            output_instruct = self.optimize_config(df_out, df_out_pred)
            print('【{}】, {}'.format(datetime.now(), output_instruct))


def test():
    logging.info('[{}] Server start'.format(datetime.now()))
    server = Server()
    server.run()


if __name__ == '__main__':
    test()
