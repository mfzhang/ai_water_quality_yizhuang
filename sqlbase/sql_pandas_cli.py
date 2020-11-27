import os
import sys
import logging
from datetime import datetime
import pymssql
from sqlalchemy import create_engine
import pandas as pd

SQL = "SET NOCOUNT ON " \
      "DECLARE @StartDate DateTime " \
      "DECLARE @EndDate DateTime " \
      "SET @StartDate = DateAdd(mi,-{},GetDate()) " \
      "SET @EndDate = GetDate() " \
      "SET NOCOUNT OFF " \
      "SELECT temp.TagName ,DateTime = convert(nvarchar, DateTime, 21) ,Value ,vValue, Unit = ISNULL(Cast(EngineeringUnit.Unit as nVarChar(20)),'N/A') ,Quality ,QualityDetail = temp.QualityDetail ,QualityString ,wwResolution ,StartDateTime From (" \
      "SELECT * " \
      "FROM History WHERE History.TagName IN ('{}') " \
      "AND wwRetrievalMode = 'Cyclic' " \
      "AND wwCycleCount = 100 " \
      "AND wwQualityRule = 'Extended' " \
      "AND wwVersion = 'Latest' " \
      "AND DateTime >= @StartDate " \
      "AND DateTime <= @EndDate) temp " \
      "LEFT JOIN AnalogTag ON AnalogTag.TagName =temp.TagName " \
      "LEFT JOIN EngineeringUnit ON AnalogTag.EUKey = EngineeringUnit.EUKey " \
      "LEFT JOIN QualityMap ON QualityMap.QualityDetail = temp.QualityDetail " \
      "WHERE temp.StartDateTime >= @StartDate"

device_dict = {
    'mf_inflow_a': {'read_name': 'MFA.JS_FT', 'write_name':	'FT101'},

    'mid_tank_level_a': {'read_name': 'LT201A.LV', 'write_name': 'LT201A'},
    'mid_tank_level_b': {'read_name': 'LT201B.LV', 'write_name': 'LT201B'},
    'out_tank_level_a': {'read_name': 'LT301A.LV', 'write_name': 'LT301A'},
    'out_tank_level_b': {'read_name': 'LT301B.LV', 'write_name': 'LT301B'},

    'alkali_injector_frequency_a': {'read_name': 'P411A.SC', 'write_name': 'SP_P411A_SC', 'chinese_name': '出水碱计量泵A频率'},
    'alkali_injector_frequency_b': {'read_name': 'P411B.SC', 'write_name': 'SP_P411B_SC', 'chinese_name': '出水碱计量泵B频率'},
    'outflow_ph': {'read_name': 'PHT201.PH_V', 'write_name': 'CIT202'},

    'deoxidant_injector_frequency_c': {'read_name': 'P409B.SP_SC', 'write_name': '_JY_P412C_FOU'},
    'deoxidant_injector_frequency_d': {'read_name': 'P412D.FOU', 'write_name': '_JY_P412D_FOU'},
    'outflow_orp': {'read_name': 'OT201.OTV', 'write_name': 'OT201'},

    'electricity': {'read_name': 'POWER_EP.EP_V1223'}
}


def decorator_pandas_read_db(func):
    def func2(*args):
        try:
            res = func(*args)
            print('[{}] successfully read data from db with {}'.format(datetime.now(), func.__name__))
            logging.info('[{}] successfully read data from db with {}'.format(datetime.now(), func.__name__))
            return res
        except Exception as e:
            print('[{}] failed to read data from db with {}, reason :{}'.format(
                datetime.now(), func.__name__, repr(e)))
            logging.info('[{}] failed to read data from db with {}'.format(
                datetime.now(), func.__name__, repr(e)))
            return 0
    return func2


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
        self._db_path = 'mssql+pymssql://{}:{}@{}/{}'.format(user, password, host, dbname)
        self._engine = create_engine(self._db_path, echo=False, pool_recycle=300)

    def get_db_data_test(self):
        sql = 'select * from result1'
        df = pd.read_sql(sql, self._engine)

    def get_db_data_by_table_name_to_df(self, table_name):
        # 测试
        logging.info('[{}] sql_pandas_cli: get data from "{}"'.format(
            datetime.now(), table_name))
        sql = 'select * from {}'.format(table_name)
        df = pd.read_sql(sql, self._engine)
        return df

    @decorator_pandas_read_db
    def get_ph_monitor_data_to_df(self):
        # get 外供水 pH 计的检测值
        # logging.info('[{}] sql_pandas_cli: get ph_monitor_data from dataset'.format(datetime.now()))
        sql = SQL.format(120, device_dict['outflow_ph']['read_name'])
        df = pd.read_sql(sql, self._engine)
        return df['Value']

    @decorator_pandas_read_db
    def get_alkali_injector_data(self):
        # get 出水碱计量泵的值
        # logging.info('[{}] sql_pandas_cli: get alkali_injector_data from dataset'.format(datetime.now()))
        sql_a = SQL.format(5, device_dict['alkali_injector_frequency_a']['read_name'])
        sql_b = SQL.format(5, device_dict['alkali_injector_frequency_b']['read_name'])
        df_a = pd.read_sql(sql_a, self._engine)
        df_b = pd.read_sql(sql_b, self._engine)
        return df_a, df_b

    @decorator_pandas_read_db
    def get_outflow_tank_level_data(self):
        # get 出水箱水位
        sql_a = SQL.format(30, device_dict['out_tank_level_a']['read_name'])
        sql_b = SQL.format(30, device_dict['out_tank_level_b']['read_name'])
        df_a = pd.read_sql(sql_a, self._engine)
        df_b = pd.read_sql(sql_b, self._engine)
        return df_a, df_b

    @decorator_pandas_read_db
    def get_mid_tank_level_data(self):
        # get 中间水箱水位
        sql_a = SQL.format(30, device_dict['mid_tank_level_a']['read_name'])
        sql_b = SQL.format(30, device_dict['mid_tank_level_b']['read_name'])
        df_a = pd.read_sql(sql_a, self._engine)
        df_b = pd.read_sql(sql_b, self._engine)
        return df_a, df_b

    @decorator_pandas_read_db
    def get_mf_inflow_data(self):
        # get 微滤进水流量
        sql = SQL.format(5, device_dict['mf_inflow_a']['read_name'])
        df = pd.read_sql(sql, self._engine)
        return df

    @decorator_pandas_read_db
    def get_electricity_past_x_hour(self, hour):
        # get 总电量
        sql = SQL.format(int(hour*60), device_dict['electricity']['read_name'])
        df = pd.read_sql(sql, self._engine)
        res = df['Value'].values[-1] - df['Value'].values[0]
        return res

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

    def write_one_row_into_output_result1(self, row):
        sql = 'select max(id) from result1'
        df_id = pd.read_sql(sql, self._engine).values[0][0]
        if df_id:
            id = df_id + 1
        else:
            id = 1
        row['id'] = [id]
        df_res = pd.DataFrame(row).set_index('id')
        df_res.to_sql('result1', con=self._engine, if_exists='append')
        a = 1

    def get_last_turns_in_result1(self):
        sql = 'select max(turns) from result1'
        df_turns = pd.read_sql(sql, self._engine).values[0][0]
        return df_turns

    def get_result1_last_two_row(self):
        sql = 'select * from result1 where id >= (select max(id)-1 from result1)'
        return pd.read_sql(sql, self._engine)

    def write_one_row_into_output_result2(self, row):
        sql = 'select max(resultId) from result2'
        df_id = pd.read_sql(sql, self._engine).values[0][0]
        if df_id:
            id = df_id + 1
        else:
            id = 1
        row['resultId'] = [id]
        df_res = pd.DataFrame(row).set_index('resultId')
        df_res.to_sql('result2', con=self._engine, if_exists='append')
        a = 1


# def test():
#     db_pandas_cli = DataBasePandasClient()
#     df = db_pandas_cli.get_db_data_by_table_name_to_df('result1')
#     print(df)

@decorator_pandas_read_db
def test_decorator():
    a = 1
    return a


def test_db_read_format():
    config_dict = {"host": "84.20.85.106", "user": "sa", "password": "monitor@333",
                   "dbname": "Runtime", "schedule_timestep_seconds": 1}

    cli = DataBasePandasClient(config_dict)
    cli.get_electricity_past_24_hour()
    df1 = cli.get_alkali_injector_data()
    df2 = cli.get_ph_monitor_data_to_df()
    df3 = cli.get_mid_tank_level_data()
    df4 = cli.get_mf_inflow_data()
    # df5 = cli.get_electricity()
    a = 1


if __name__ == '__main__':
    test_db_read_format()
    # test_decorator()
    # test()

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