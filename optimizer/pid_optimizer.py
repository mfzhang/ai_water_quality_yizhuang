import logging
from datetime import datetime
from sqlbase.sql_cli import DataBaseSqlClient
from src.constants import PhStandard
import random


class PidOptimizer(object):
    def __init__(self):
        pass

    @staticmethod
    def optimize_config_with_pid(df_out, df_out_pred):
        standard = 80
        if df_out['value1'].mean() > standard:
            return 'reduce injector'
        else:
            return 'augment injector'

    @staticmethod
    def write_result(self, rows):
        logging.info('[{}] write result 【{}】 into OutputDB'.format(
            datetime.now(), rows
        ))
        db_sql_cli = DataBaseSqlClient()
        db_sql_cli.write_rows_into_output_table(rows)

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

    def optimizer_mf_by_outflow_with_pid(self, df_outflow):
        result = {
            'device': 'JYDY1',
            'parameter': '酸泵',
            'originalValue': 0,
            'newValue': 0
        }
        return result


def test():
    pass


if __name__ == '__main__':
    test()
