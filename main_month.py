# 주택용 계산일 경우 일차원 배열 사용

from UserData import *
from CalcHome import *
from CalcGeneral import *
from CalcIndustry import *

used_amount_list = [1 for i in range(12)]
contract_demand = 0
charge = 0
voltage_factor = 0
class1 = 0
class2 = 0
class_contract = 0
i = 1

user_data = UserData(used_amount_list, contract_demand, charge, voltage_factor,
                     class1, class2, class_contract)

calc = CalcHome(user_data.used_amount_list, user_data.voltage_factor)
print(int(calc.init_calc_month(i)))