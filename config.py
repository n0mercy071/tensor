import configparser


class Config():
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.path = path
        self.config.read(path)

    def get_value(self, partition, value_name):
        return self.config.get(partition, value_name)
