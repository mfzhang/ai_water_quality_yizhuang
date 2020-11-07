# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 9:34
# @Author  : MA Ziqing
# @FileName: constants.py.py


import gflags
flags = gflags.FLAGS
gflags.DEFINE_integer('server_time_interval', 5, 'time interval of server run, default=?s')
gflags.DEFINE_integer('version', 0, '0 is normal version and 1 is backup version')


class Columns(object):
    pump1 = 'PUMP1'


class WaterQualityStandard(object):
    TRANSPARENCY = 1  # 透明度
    CONDUCTIVITY = 1  # 电导率
    TURBIDITY = 1  # 浊度
    PH = 7  # pH
    CHLORINE = 1  # 余氯
    ORT = 1  # 氧化还原电位 oxidation-reduction titration


class WaterQualityMaxLim(object):
    TRANSPARENCY = 1.1
    CONDUCTIVITY = 1.1
    TURBIDITY = 1.1
    pH = 7.1
    CHLORINE = 1.1
    ORT = 1.1

class PhStandard(object):
    STANDARD = 6.5
    MAXLIMIT = 6.6
    MINLIMIT = 6.4
