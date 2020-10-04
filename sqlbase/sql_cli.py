# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:25
# @Author  : MA Ziqing
# @FileName: sql_cli.py.py

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlbase.sql_table_base import QualityIndicator


class DataBaseClient(object):
    def __init__(self):
        self._db_name = 'foo.db'
        self._db_path = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\' + self._db_name
        self._engine = create_engine(self._db_path, echo=True)

    def get_quality_indicator_data(self):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        query = session.query(QualityIndicator)
        query.filter(QualityIndicator.value1 > 50)
        return query


def test():
    data_base_cli = DataBaseClient()
    query = data_base_cli.get_quality_indicator_data()
    for qi in query:
        print(qi)


if __name__ == '__main__':
    test()
