import logging
from datetime import datetime
# from sqlbase.sql_cli import DataBaseSqlClient
from src.constants import PhStandard
import random
from sqlbase.sql_pandas_cli import device_dict


class PidOptimizer(object):
    def __init__(self):
        pass

    def optimize_ph_with_pid(self, df_ph=None, alkali_injector=None):
        a, b = alkali_injector.get_current_value()
        average_ph = df_ph.mean()
        delta = 0.1
        if 1 < average_ph < 13:
            if df_ph.mean() > PhStandard.MAXLIMIT:
                alkali_injector.set_new_value(a-delta, b-delta)
            elif df_ph.mean() < PhStandard.MINLIMIT:
                alkali_injector.set_new_value(a+delta, b+delta)
            else:
                alkali_injector.set_new_value(a, b)
        else:
            alkali_injector.set_new_value(a, b)
        result, drug_pred = alkali_injector.get_result_and_drug_predict()
        return result, drug_pred

    def optimze_deoxidant_by_orp_with_pid(self, df_orp=None):
        new_values = random.randint(1, 4)
        drug_pred = random.randint(1, 5)/100
        result_increase = {
            'device': 'LT411A',
            'parameter': 'unknown',
            'originalValue': 'unknown',
            'newValue': '+' + str(new_values / 10)
        }
        result_reduce = {
            'device': 'LT411A',
            'parameter': 'unknown',
            'originalValue': 'unknown',
            'newValue': '-' + str(new_values / 10)
        }
        if df_orp:
            if df_orp.max() > PhStandard.MAXLIMIT:
                return result_reduce
            elif df_orp.min() < PhStandard.MINLIMIT:
                return result_increase
            else:
                return None
        else:
            return random.choice([result_increase, result_reduce, None]), drug_pred

    def optimizer_mf_by_outflow_with_pid(self, df_inflow=None, df_outflow=None):
        df_inflow_mean = df_inflow['Value'].mean()
        res = {'id': -1,
               'turns': -1,
               'time': '',
               'device': device_dict['mf_inflow_a']['write_name'],
               'parameter': device_dict['mf_inflow_a']['chinese_name'],
               'originalValue': df_inflow_mean,
               'newValue': df_inflow_mean,
               'change': 0,
               'state': 1,
               'type': 1}
        energy_pred = 10
        return [res], energy_pred


def test():
    pass


if __name__ == '__main__':
    test()
