from abc import *
import json
import os
import sys


class CalcCharge(metaclass=ABCMeta):
    @abstractmethod
    def init_calc(self):
        pass

    @staticmethod
    def get_conf(self):     # 환경부담금, 연료비조정액 가져오기
        print(os.getcwd())
        if os.path.exists('conf.json'):     # Parser 의 경로 문제 대응
            with open(os.path.abspath('conf.json')) as f:
                config = json.load(f)
        else:
            with open(os.path.abspath('..\\conf.json')) as f:
                config = json.load(f)
        return float(config['env_contribution']), float(config['fuel_rate'])



