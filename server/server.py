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
from src.constants import flags
# logging.basicConfig(filename='server.log', level=logging.DEBUG)


class Server(object):
    def __init__(self, config_dict=None):
        # print('Server initialized in version ', flags.version)
        if flags.version == 0:
            try:
                self._db_pandas_cli = DataBasePandasClient(config_dict)
            except Exception:
                print('db connection failed, server restart in version 1')
                flags.version = 1
        self._pre_treat_pandas = PreTreatPandas()
        self._pid_optimizer = PidOptimizer()

    # def get_input_data(self):
    #     table_name = INJECTOR_LIST[0].__tablename__
    #     return self._db_pandas_cli.get_db_data_by_table_name_to_df(table_name)
    #
    # def get_label_data(self):
    #     table_name = INDICATOR_LIST[0].__tablename__
    #     return self._db_pandas_cli.get_db_data_by_table_name_to_df(table_name)
    #
    # def pre_treat_input_data(self, df):
    #     return self._pre_treat_pandas.mask_extreme_value(df)
    #
    # def treat_with_ml_model(self, df):
    #     return df
    #
    # def optimize_config(self, df_out, df_out_pred):
    #     output_instruct = self._pid_optimizer.optimize_config_with_pid(df_out, df_out_pred)
    #     return output_instruct
    #
    # def run_simulation(self):
    #     df_inp = self.get_input_data()
    #     df_inp = self.pre_treat_input_data(df_inp)
    #     df_out_pred = self.treat_with_ml_model(df_inp)
    #     df_out = self.get_label_data()
    #     output_instruct = self.optimize_config(df_out, df_out_pred)
    #     logging.info('[{}], {}'.format(datetime.now(), output_instruct))

    def ph_optimizer_run(self):
        # pH 优化模块：利用负反馈调节使出水 pH 在 6.5 附近变动
        if flags.version == 0:
        # df_ph = None
        # df_pump = None
        # if self._db_pandas_cli is not None:
            print('server start with version 0')
            df_ph = self._db_pandas_cli.get_ph_monitor_data_to_df()
            df_ph = self._pre_treat_pandas.mask_extreme_value(df_ph)
            df_pump = None
            result = self._pid_optimizer.optimize_ph_with_pid(df_ph, df_pump)
        elif flags.version == 1:
            print('server start with version 1')
            result = self._pid_optimizer.optimize_ph_with_pid(df_ph=None, df_pump=None)
        else:
            print('server version false', flags.version)
            result = None
        print('schedule result: ', result)
        return result

    def qmf_optimizer_run(self):
        # quantity_micro_filter 微滤进水流量优化模块：使进水与出水相当
        df_outflow = self._db_pandas_cli.get_outflow_quantity_data()
        df_outflow = self._pre_treat_pandas.mask_extreme_value(df_outflow)
        result = self._pid_optimizer.optimizer_mf_by_outflow_with_pid(df_outflow)
        return result

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

    def run_real(self):
        result_list = []

        json_res_ph = self.ph_optimizer_run()
        if json_res_ph:
            result_list += [json_res_ph]

        json_res_xxx = self.qmf_optimizer_run()
        if json_res_xxx:
            result_list += [json_res_xxx]

        self.write_result(result_list)


def test():
    logging.info('[{}] Server start'.format(datetime.now()))
    server = Server()
    server.run_real()


if __name__ == '__main__':
    test()
