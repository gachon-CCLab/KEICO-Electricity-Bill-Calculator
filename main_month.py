# 주택용 계산일 경우 일차원 배열 사용

from UserData import *
from CalcHome import *
from CalcGeneral import *
from CalcIndustry import *

# data input
used_amount_list = [[1 for i in range(3)] for j in range(12)]
contract_demand = 0
charge = 0
voltage_factor = 0
class1 = 0
class2 = 0
class_contract = 0
month = 12

user_data = UserData(used_amount_list, contract_demand, charge, voltage_factor,
                     class1, class2, class_contract)

calc_type = int(input("계산 유형을 선택하세요.\n1. 주택\n2. 일반\n3. 산업\n"))

# 계약종별 분기
if calc_type == 1:
    temp_list = [list(x) for x in zip(*user_data.used_amount_list)]   # 리스트 전치
    user_data.used_amount_list = temp_list[0]
    calc = CalcHome(user_data.used_amount_list, user_data.voltage_factor)
    print(int(calc.init_calc_month(month-1)))
elif calc_type == 2:
    calc = CalcGeneral(user_data.used_amount_list, user_data.contract_demand,
                       user_data.class1, user_data.class2, user_data.class_contract)
    print(int(calc.init_calc_month(month-1)))
elif calc_type == 3:
    calc = CalcIndustry(user_data.used_amount_list, user_data.contract_demand,
                        user_data.class1, user_data.class2, user_data.class_contract)
    print(int(calc.init_calc_month(month-1)))
else:
    print("잘못된 입력입니다.")