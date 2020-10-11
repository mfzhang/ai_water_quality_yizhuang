import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlbase.sql_table_base import QualityIndicator, ALL_LIST

import pandas as pd


class DataBasePandasClient(object):
    def __init__(self):
        self._db_name = 'foo.db'
        self._db_path = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\' + self._db_name
        self._engine = create_engine(self._db_path, echo=False)

    def get_quality_indicator_data(self, table_name):
        logging.info('[{}] get data from "{}"'.format(
            datetime.now(), table_name))
        sql = 'select * from {}'.format(table_name)
        df = pd.read_sql(sql, self._engine)
        return df

    def get_ph_monitor_data(self):
        logging.info('[{}] get data from dataset'.format(datetime.now()))
        sql = 'SELECT * FROM AnalogTag, EngineeringUnit, Tag ' \
              'where Tag.TagName IN (xxx.ph) ' \
              'AND Tag.TagName=AnalogTag.TagName ' \
              'AND AnalogTaag.EUKey = EngineeringUnit.EUKey'
        df = pd.read_sql(sql, self._engine)
        return df


def test():
    db_pandas_cli = DataBasePandasClient()
    df = db_pandas_cli.get_quality_indicator_data(ALL_LIST[0].__tablename__)
    print(df)


if __name__ == '__main__':
    test()
