# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:26
# @Author  : MA Ziqing
# @FileName: server.py.py
import os
import logging
from datetime import datetime
from sqlbase.sql_pandas_cli import DataBasePandasClient
from sqlbase.sql_cli import DataBaseSqlClient
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

    def run_simulation(self):
        # counter_max = 5
        # counter = 0
        # while True:
        #     counter += 1
        #     if counter > counter_max:
        #         break
        df_inp = self.get_input_data()
        df_inp = self.pre_treat_input_data(df_inp)
        df_out_pred = self.treat_with_ml_model(df_inp)
        df_out = self.get_label_data()
        output_instruct = self.optimize_config(df_out, df_out_pred)
        logging.info('[{}], {}'.format(datetime.now(), output_instruct))

    def ph_optimizer_run(self):
        # pH 优化模块：利用负反馈调节使出水 pH 在 6.5 附近变动
        df_ph = self._db_pandas_cli.get_ph_monitor_data()
        df_ph = self._pre_treat_pandas.mask_extreme_value(df_ph)
        result = self._pid_optimizer.optimize_ph_with_pid(df_ph)
        return result

    def xxx_optimizer_run(self):
        return None

    def run_real(self):
        result_list = []

        json_res_ph = self.ph_optimizer_run()
        if json_res_ph is not None:
            result_list += [json_res_ph]

        json_res_xxx = self.xxx_optimizer_run()
        if json_res_xxx is not None:
            result_list += [json_res_xxx]

        self.write_result(result_list)

    @staticmethod
    def write_result(result_list):
        logging.info('[{}] write result 【{}】 into OutputDB'.format(
            datetime.now(), result_list
            ))
        rows = {'id': 1,
                'time': datetime.now(),
                'energyPred': 10.2,
                'drugPred': 7.8,
                'deviceList': result_list,
                'state': 1,
                'type': 1
                }
        db_sql_cli = DataBaseSqlClient()
        db_sql_cli.write_rows_into_output_table(rows)


def test():
    logging.info('[{}] Server start'.format(datetime.now()))
    server = Server()
    server.run_simulation()


if __name__ == '__main__':
    test()
