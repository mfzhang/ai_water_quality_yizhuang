

class PidOptimizer(object):
    def __init__(self):
        pass

    def optimize_config_with_pid(self, df_out, df_out_pred):
        standard = 80
        if df_out['value1'].mean() > standard:
            return 'reduce injector'
        else:
            return 'augment injector'


def test():
    pass


if __name__ == '__main__':
    test()