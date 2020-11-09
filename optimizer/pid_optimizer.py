import logging
from datetime import datetime
# from sqlbase.sql_cli import DataBaseSqlClient
from src.constants import PhStandard
import random


class PidOptimizer(object):
    def __init__(self):
        pass

    def optimize_ph_with_pid(self, df_ph, df_pump):
        new_values = random.randint(1, 4)
        result_increase = {
            'device': 'P410A',
            'parameter': 'unknown',
            'originalValue': 'unknown',
            'newValue': '+' + str(new_values/10)
        }
        result_reduce = {
            'device': 'P410A',
            'parameter': 'unknown',
            'originalValue': 'unknown',
            'newValue': '-' + str(new_values / 10)
        }
        if df_ph:
            if df_ph.max() > PhStandard.MAXLIMIT:
                return result_reduce
            elif df_ph.min() < PhStandard.MINLIMIT:
                return result_increase
            else:
                return None
        else:
            return random.choice([result_increase, result_reduce, None])

    def optimze_deoxidant_by_orp_with_pid(self, df_orp=None):
        new_values = random.randint(1, 4)
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
            return random.choice([result_increase, result_reduce, None])

    def optimizer_mf_by_outflow_with_pid(self, df_outflow=None):
        new_values = random.randint(0, 1)
        result_increase = {
            'device': 'RO套数',
            'parameter': 'unknown',
            'originalValue': 'unknown',
            'newValue': '增加{}套'.format(new_values)
        }
        result_reduce = {
            'device': 'RO套数',
            'parameter': 'unknown',
            'originalValue': 'unknown',
            'newValue': '减少{}套'.format(new_values)
        }
        return random.choice([result_increase, result_reduce, None])


def test():
    pass


if __name__ == '__main__':
    test()
