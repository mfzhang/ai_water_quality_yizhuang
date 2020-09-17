# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 0:32
# @Author  : MA Ziqing
# @FileName: main.py


def run():

    sqlbase.read_input_data()

    server.serve(model)

    optimizer.optimize()


if __name__ == '__main__':
    run()
