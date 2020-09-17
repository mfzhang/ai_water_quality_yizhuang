# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:25
# @Author  : MA Ziqing
# @FileName: sqlbase.py.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_engine():
    pass


class DataBaseClient(object):
    def __init__(self):
        self._data_base_url = 'sqlite:///orm_in_detail.sqlite'
        self._engine = create_engine(self._data_base_url)


    def get_input_data(self):
        session = sessionmaker()
        session.configure(bind=self._engine)
        s = session()

        pass

    def get_serving_input_data(self):
        pass

    def write_result(self):
        pass


def test():
    pass


if __name__ == '__main__':
    test()
