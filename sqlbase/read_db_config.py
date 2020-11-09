import json


def read_db_config():
    # config_dict = dict()
    # path = os.path.abspath(__file__)
    # print('read_db abspath', path)
    with open('./config.txt', 'r') as f:
        text = f.read()
        config_dict = json.loads(text)
    #     text_list = text.split('\n')
    # config_dict['host'] = text_list[0]
    # config_dict['user'] = text_list[1]
    # config_dict['password'] = text_list[2]
    # config_dict['dbname'] = text_list[3]
    return config_dict


if __name__ == '__main__':
    config_dict = read_db_config()
    print(config_dict)
