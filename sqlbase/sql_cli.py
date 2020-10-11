# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:25
# @Author  : MA Ziqing
# @FileName: sql_cli.py.py

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlbase.sql_table_base import QualityIndicator, OutputDB, Result1, Result2


class DataBaseSqlClient(object):
    def __init__(self):
        self._db_name = 'foo.db'
        self._db_path = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\' + self._db_name
        self._engine = create_engine(self._db_path, echo=False)

    def get_quality_indicator_data(self):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        query = session.query(QualityIndicator)
        query.filter(QualityIndicator.value1 > 50)
        return query

    def write_rows_into_output_table(self, rows):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        res_list = []
        for row in rows:
            res = OutputDB(timestamp=row['timestamp'],
                           device=row['device'],
                           status=row['status'],
                           instruction=row['instruction'])
            res_list += [res]
        session.add_all(res_list)
        session.commit()

    def write_one_row_into_output_result1(self, row):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        res = Result1(id=row['id'],
                      json=row['json'],
                      state=row['state'],
                      type=row['type'])
        session.add_all(res)
        session.commit()

    def write_one_row_into_output_result2(self, row):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        res = Result2(resultId=row['id'],
                      json=row['json'],
                      state=row['state'],
                      type=row['type'])
        session.add_all(res)
        session.commit()


def test():
    data_base_cli = DataBaseSqlClient()
    query = data_base_cli.get_quality_indicator_data()
    for qi in query:
        print(qi)


if __name__ == '__main__':
    test()
