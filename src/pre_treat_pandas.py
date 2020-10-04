# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:29
# @Author  : MA Ziqing
# @FileName: pre_treat_pandas.py

import numpy as np
import pandas as pd


class PreTreatPandas(object):
    def __init__(self):
        self.name = 'PreProcessor'

    def mask_extreme_value(self, df):
        default_column = df.columns[1]
        upper_bound = df[default_column].quantile(0.9)
        lower_bound = df[default_column].quantile(0.1)
        replace_value = df[default_column].mean()
        df[df[default_column] > upper_bound] = replace_value
        df[df[default_column] < lower_bound] = replace_value
        return df

    def get_the_rolling_mean(self, df):
        df_ = df.rolling(2).mean().dropna()
        return df_


def test():
    df = pd.DataFrame({'value1': [1, 2, 3, 4, 5, 6], 'value2': [2]*6})
    print('the original df is {}'.format(df))
    pre_treat_pandas = PreTreatPandas()
    df = pre_treat_pandas.mask_extreme_value(df)
    df = pre_treat_pandas.get_the_rolling_mean(df)
    print('the pre-treated df is {}'.format(df))


if __name__ == '__main__':
    test()

