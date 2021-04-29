from abc import *
import json


class CalcCharge(metaclass=ABCMeta):
    @abstractmethod
    def init_calc(self):
        pass

    @staticmethod
    def get_conf(self): # 환경부담금, 연료비조정액 가져오기
        with open('conf.json') as f:
            config = json.load(f)
        return float(config['env_contribution']), float(config['fuel_rate'])



