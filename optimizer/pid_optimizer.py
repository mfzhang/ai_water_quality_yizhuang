import logging
from sqlbase.sql_cli import DataBaseSqlClient


class PidOptimizer(object):
    def __init__(self):
        pass

    @staticmethod
    def optimize_config_with_pid(self, df_out, df_out_pred):
        standard = 80
        if df_out['value1'].mean() > standard:
            return 'reduce injector'
        else:
            return 'augment injector'

    @staticmethod
    def write_result(self, rows):
        db_sql_cli = DataBaseSqlClient()
        db_sql_cli.write_rows_into_output_table(rows)




def test():
    pass


if __name__ == '__main__':
    test()