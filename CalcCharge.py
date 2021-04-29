from abc import *
import json


class CalcCharge(metaclass=ABCMeta):
    @abstractmethod
    def init_calc(self):
        pass

    @staticmethod
    def get_conf(self):
        with open('conf.json') as f:
            config = json.load(f)
        return config['env_contribution'], config['fuel_rate']



