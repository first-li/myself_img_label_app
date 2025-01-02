import os

import yaml


def get_config():
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, 'config.yaml')
    # 打开并读取YAML文件
    with open(config_path, 'r') as file:
        config_file = yaml.safe_load(file)
    return config_file


class Config:
    def __init__(self):
        self.config = get_config()
        window_size = self.config.get('window_size', [800, 600])  # 提供默认值以防配置缺失
        # 将列表解包成两个变量
        self.window_width, self.window_height = window_size


config = Config()



