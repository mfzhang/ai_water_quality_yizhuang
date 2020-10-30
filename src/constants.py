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

# class PhStandard(object):
#     STANDARD = 6.5
#     MAXLIMIT = 6.6
#     MINLIMIT = 6.4
