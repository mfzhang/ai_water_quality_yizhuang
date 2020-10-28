import logging
from datetime import datetime
from sqlbase.sql_cli import DataBaseSqlClient
from src.constants import PhStandard


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

    def optimize_ph_with_pid(self, df_ph):
        result = {}
        if df_ph.max() > PhStandard.MAXLIMIT:
            result = {
                'device': 'JYDY1',
                'parameter': '酸泵',
                'originalValue': 0,
                'newValue': 0
            }
        elif df_ph.min() < PhStandard.MINLIMIT:
            result = {
                'device': 'JYDY1',
                'parameter': '碱泵',
                'originalValue': 0,
                'newValue': 0
            }
        return result

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
