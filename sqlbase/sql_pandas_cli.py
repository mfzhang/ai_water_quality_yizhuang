import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlbase.sql_table_base import QualityIndicator

import pandas as pd


class DataBasePandasClient(object):
    def __init__(self):
        self._db_name = 'foo.db'
        self._db_path = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\' + self._db_name
        self._engine = create_engine(self._db_path, echo=True)

    def get_quality_indicator_data(self):
        sql = '''
        select * from quality_indicator_1
        '''

        df = pd.read_sql(sql, self._engine)
        return df


def test():
    db_pandas_cli = DataBasePandasClient()
    df = db_pandas_cli.get_quality_indicator_data()
    print(df)


if __name__ == '__main__':
    test()
