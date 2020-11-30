
from sqlbase.sql_pandas_cli import device_dict, DataBasePandasClient
from src.constants import PhStandard


class ParameterBase(object):
    def __init__(self, parameter_name):
        self._paramter_name = parameter_name
        self._cur_value = -1
        self._new_value = -1
        self._return_res = {'id': -1,
                            'turns': -1,
                            'time': '',
                            'device': device_dict[parameter_name]['write_name'],
                            'parameter': device_dict[parameter_name]['chinese_name'],
                            'originalValue': -1,
                            'newValue': -1,
                            'change': 0,
                            'state': 1,
                            'type': -1}

    def __repr__(self):
        return '【{}】 cur_value: {}, new_value:{}'.format(self._paramter_name, self._cur_value, self._new_value)

    def set_cur_value(self, cur_value):
        self._cur_value = cur_value

    def get_cur_value(self):
        return self._cur_value

    def update_cur_value(self, cli):
        self._cur_value = cli.get_current_data_mean_of_1min_by_device_name(device_dict[self._paramter_name]['read_name'])

    def set_new_value(self, new_value):
        self._new_value = new_value

    def get_new_value(self):
        return self._new_value

    def get_return_result(self):
        self._return_res['originalValue'] = self.get_cur_value()
        self._return_res['newValue'] = self.get_new_value()
        return self._return_res