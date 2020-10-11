# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 9:34
# @Author  : MA Ziqing
# @FileName: constants.py.py


class Columns(object):
    pump1 = 'PUMP1'


class WaterQualityStandard(object):
    TRANSPARENCY = 1  # 透明度
    CONDUCTIVITY = 1  # 电导率
    TURBIDITY = 1  # 浊度


class PhStandard(object):
    STANDARD = 6.5
    MAXLIMIT = 6.6
    MINLIMIT = 6.4
