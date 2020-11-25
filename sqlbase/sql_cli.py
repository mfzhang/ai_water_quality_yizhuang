# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:25
# @Author  : MA Ziqing
# @FileName: sql_cli.py.py
#
# import os
# import sys
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlbase.sql_table_base import QualityIndicator, OutputDB, Result1, Result2
#
#
# class DataBaseSqlClient(object):
#     def __init__(self, config_dict):
#         user = config_dict['user']  # 'sa'
#         dbname = config_dict['dbname']  # 'YZSC'
#         host = config_dict['host']  # '166.111.42.116'
#         password = config_dict['password']  # '123456'
#         # mysql + pymysql: // < username >: < password > @ < host > / < dbname > charset = utf8
#         self._db_path_2 = 'mssql+pymssql://{}:{}@{}/{}'.format(user, password, host, dbname)
#         self._engine = create_engine(self._db_path_2, echo=False)
#
#     def get_quality_indicator_data(self):
#         Session = sessionmaker(bind=self._engine)
#         session = Session()
#         query = session.query(QualityIndicator)
#         query.filter(QualityIndicator.value1 > 50)
#         return query
#
#     def write_one_row_into_output_result1(self, row):
#         Session = sessionmaker(bind=self._engine)
#         session = Session()
#         last_row = session.query(Result1).order_by(Result1.id.desc()).first()
#         res = Result1()
#         if last_row:
#             res.id = last_row.id + 1
#         else:
#             res.id = 0
#         res.json = row['json']
#         res.state = row['state']
#         res.type = row['type']
#         session.add(res)
#         session.commit()
#
#     def write_one_row_into_output_result2(self, row):
#         Session = sessionmaker(bind=self._engine)
#         session = Session()
#         res = Result2(resultId=row['id'],
#                       json=row['json'],
#                       state=row['state'],
#                       type=row['type'])
#         session.add(res)
#         session.commit()
#
#
# def test():
#     data_base_cli = DataBaseSqlClient()
#     query = data_base_cli.get_quality_indicator_data()
#     for qi in query:
#         print(qi)
#
#
# if __name__ == '__main__':
#     test()
