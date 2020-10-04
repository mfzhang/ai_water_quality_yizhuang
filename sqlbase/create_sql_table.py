import os
import sys
from datetime import datetime
from random import random

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlbase.sql_table_base import QualityIndicator, INDICATOR_LIST
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///:memory:', echo=True)
# Base = declarative_base()


class DbRandomCreator(object):
    def __init__(self):
        self._db_name = 'foo.db'
        self._db_path = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\' + self._db_name
        self._engine = create_engine(self._db_path, echo=True)

    def create_all_table_randomly(self):
        time_start = int(datetime.now().timestamp())
        time_end = time_start + 15 * 60 * 100
        time_interval = 15 * 60
        time_tuple = (time_start, time_end, time_interval)
        for table in INDICATOR_LIST:
            self.create_one_table_randomly(table, time_tuple)

    def create_one_table_randomly(self, table, time_tuple):
        table.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        session = Session()
        time_start, time_end, time_interval = time_tuple
        sample_list = []
        for timestamp in range(time_start, time_end, time_interval):
            value1 = int(random() * 100)
            value2 = int(random() * 100)
            sample = table(timestamp=timestamp,
                           value1=value1,
                           value2=value2,
                           status='ok')
            sample_list += [sample]
        session.add_all(sample_list)
        session.commit()


if __name__ == '__main__':
    db_random_creator = DbRandomCreator()
    db_random_creator.create_all_table_randomly()
