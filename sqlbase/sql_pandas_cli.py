import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlbase.sql_table_base import QualityIndicator, ALL_LIST

import pandas as pd


class DataBasePandasClient(object):
    '''
    需要监测的点位：
    PHT301 回用水外供水pH计 SP_PHT301
    P411A/B/C 出水碱计量泵A/B/C SP_P411A/B/_SC

    ?  外供流量
    SP_FT109 超滤进水调节阀A-I

    ? 微滤运行时间 SET_MFX_RUN_TIME
    ? 微滤前的压力
    '''
    def __init__(self, config_dict):
        # self._db_name = 'foo.db'
        # self._db_path = 'sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '\\' + self._db_name
        user = config_dict['user']  # 'sa'
        dbname = config_dict['dbname']  # 'YZSC'
        host = config_dict['host']  # '166.111.42.116'
        password = config_dict['password']  # '123456'
        # mysql + pymysql: // < username >: < password > @ < host > / < dbname > charset = utf8
        self._db_path_2 = 'mssql+pymssql://{}:{}@{}/{}'.format(user, password, host, dbname)
        self._engine = create_engine(self._db_path_2, echo=False)

    def get_db_data_by_table_name_to_df(self, table_name):
        # 测试
        logging.info('[{}] sql_pandas_cli: get data from "{}"'.format(
            datetime.now(), table_name))
        sql = 'select * from {}'.format(table_name)
        df = pd.read_sql(sql, self._engine)
        return df

    def get_ph_monitor_data_to_df(self):
        # get 外供水 pH 计的检测值
        logging.info('[{}] sql_pandas_cli: get ph_monitor_data from dataset'.format(datetime.now()))
        sql = "SELECT TagName = Tag.TagName, Description = Tag.Description, ' \
              'MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType ' \
              'FROM AnalogTag, EngineeringUnit, Tag ' \
              'WHERE Tag.TagName IN ('PHT301.PH_V') ' \
              'AND Tag.TagName = AnalogTag.TagName A' \
              'ND AnalogTag.EUKey = EngineeringUnit.EUKey"
        df = pd.read_sql(sql, self._engine)
        return df

    def get_alkali_injector_data(self):
        # get 出水碱计量泵的值
        logging.info('[{}] sql_pandas_cli: get alkali_injector_data from dataset'.format(datetime.now()))
        sql = 'SELECT * FROM AnalogTag, EngineeringUnit, Tag ' \
              'where Tag.TagName IN (xxx.ph) ' \
              'AND Tag.TagName=AnalogTag.TagName ' \
              'AND AnalogTaag.EUKey = EngineeringUnit.EUKey'
        df = pd.read_sql(sql, self._engine)
        return df

    def get_outflow_quantity_data(self):
        # get 出水总流量的值
        logging.info('[{}] sql_pandas_cli: get outflow_quantity_data from dataset'.format(datetime.now()))
        sql = 'SELECT * FROM AnalogTag, EngineeringUnit, Tag ' \
              'where Tag.TagName IN (xxx.ph) ' \
              'AND Tag.TagName=AnalogTag.TagName ' \
              'AND AnalogTaag.EUKey = EngineeringUnit.EUKey'
        df = pd.read_sql(sql, self._engine)
        return df

    def get_runtime_mf_data(self):
        # get 微滤运行时间
        logging.info('[{}] sql_pandas_cli: get runtime_mf_data from dataset'.format(datetime.now()))
        sql = 'SELECT * FROM AnalogTag, EngineeringUnit, Tag ' \
              'where Tag.TagName IN (xxx.ph) ' \
              'AND Tag.TagName=AnalogTag.TagName ' \
              'AND AnalogTaag.EUKey = EngineeringUnit.EUKey'
        df = pd.read_sql(sql, self._engine)
        return df

    def get_pressure_before_mf_data(self):
        # get 微滤前压力
        logging.info('[{}] sql_pandas_cli: get pressure_before_mf_data from dataset'.format(datetime.now()))
        sql = 'SELECT * FROM AnalogTag, EngineeringUnit, Tag ' \
              'where Tag.TagName IN (xxx.ph) ' \
              'AND Tag.TagName=AnalogTag.TagName ' \
              'AND AnalogTaag.EUKey = EngineeringUnit.EUKey'
        df = pd.read_sql(sql, self._engine)
        return df

    def get_chlorine_before_ro_data(self):
        logging.info('[{}] sql_pandas_cli: get pressure_before_mf_data from dataset'.format(datetime.now()))
        sql = "SELECT TagName = Tag.TagName, Description = Tag.Description, " \
              "MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType " \
              "FROM AnalogTag, EngineeringUnit, Tag " \
              "WHERE Tag.TagName IN ('CLT301.CLT_V') " \
              "AND Tag.TagName = AnalogTag.TagName " \
              "AND AnalogTag.EUKey = EngineeringUnit.EUKey"
        df = pd.read_sql(sql, self._engine)
        return df


def test():
    db_pandas_cli = DataBasePandasClient()
    df = db_pandas_cli.get_db_data_by_table_name_to_df('result1')
    print(df)


if __name__ == '__main__':
    test()

'''
笔记
----------
中间水箱
液位：LT201A
控制微滤进水调节
----------
外供水箱 
液位：LT301A
     LT301B
控制：RO套数
     
PH：  PHT202
碱泵：  P410A/B P411 控制 Hz，调+-0.5 （加在RO前）
流量： FT301
回水泵 P303A,B,C P302, P301
-----------
微滤
进水: FT101（PID_YA101A），103，105，107，109，111
正洗，反洗 ？
-----------
反渗透 ORP OT201 
控制还原剂 LT411A/B/C （加在RO前）

'''

'''
出水外供pH
SELECT TagName = Tag.TagName, Description = Tag.Description, MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType
 FROM AnalogTag, EngineeringUnit, Tag
 WHERE Tag.TagName IN ('PHT301.PH_V')
 AND Tag.TagName = AnalogTag.TagName
 AND AnalogTag.EUKey = EngineeringUnit.EUKey

反渗透A产水 （A到G：ROA到ROG）
SELECT TagName = Tag.TagName, Description = Tag.Description, MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType
 FROM AnalogTag, EngineeringUnit, Tag
 WHERE Tag.TagName IN ('USER_SUM_INPUT_OUTPUT.ROA_CS_FT')
 AND Tag.TagName = AnalogTag.TagName
 AND AnalogTag.EUKey = EngineeringUnit.EUKey

微滤A进水 （A到F：MFA到MFF）
SELECT TagName = Tag.TagName, Description = Tag.Description, MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType
 FROM AnalogTag, EngineeringUnit, Tag
 WHERE Tag.TagName IN ('MFA.JS_FT')
 AND Tag.TagName = AnalogTag.TagName
 AND AnalogTag.EUKey = EngineeringUnit.EUKey

超滤压差（A到F：MFA-MFD）
SELECT TagName = Tag.TagName, Description = Tag.Description, MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType
 FROM AnalogTag, EngineeringUnit, Tag
 WHERE Tag.TagName IN ('MFD.yacha_PV')
 AND Tag.TagName = AnalogTag.TagName
 AND AnalogTag.EUKey = EngineeringUnit.EUKey


出水余氯仪
SELECT TagName = Tag.TagName, Description = Tag.Description, MinRaw, MaxRaw, Unit, MinEU, MaxEU, StorageRate, StorageType
 FROM AnalogTag, EngineeringUnit, Tag
 WHERE Tag.TagName IN ('CLT301.CLT_V')
 AND Tag.TagName = AnalogTag.TagName
 AND AnalogTag.EUKey = EngineeringUnit.EUKey
 氯
碱 出水  微滤
'''