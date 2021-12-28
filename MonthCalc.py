from UserData import *
from CalcHome import *
from CalcGeneral import *
from CalcIndustry import *


class MonthCalc:
    def __init__(self):
        used_amount_list = [[1 for i in range(3)] for j in range(12)]
        contract_demand = 0
        charge = 0
        voltage_factor = 0
        calc_type = 1
        class1 = 0
        class2 = 1
        class_contract = 0

        self.user_data = UserData(used_amount_list, contract_demand, charge, voltage_factor,
                                  calc_type, class1, class2, class_contract)

    def get_result(self, user_data: UserData, month) -> float:
        if user_data is not None:
            # data input
            self.user_data = user_data

        # calc_type = int(input("계산 유형을 선택하세요.\n1. 주택\n2. 일반\n3. 산업\n"))
        # 임의값. 실제 데이터 입력 시 수정 필요
        # self.calc_type = 1
        # month = 12

        # 계약종별 분기
        if self.user_data.calc_type == 1:
            temp_list = [list(x) for x in zip(*self.user_data.used_amount_list)]  # 리스트 전치
            used_amount_list_for_home = temp_list[0]  # 주택용 계산일 경우 일차원 배열 사용
            calc = CalcHome(used_amount_list_for_home, self.user_data.voltage_factor)
            print(int(calc.init_calc_month(month - 1)))
            result = calc.init_calc_month(month - 1)
        elif self.user_data.calc_type == 2:
            calc = CalcGeneral(self.user_data.used_amount_list, self.user_data.contract_demand,
                               self.user_data.class1, self.user_data.class2, self.user_data.class_contract)
            print(int(calc.init_calc_month(month - 1)))
            result = calc.init_calc_month(month - 1)
        elif self.user_data.calc_type == 3:
            calc = CalcIndustry(self.user_data.used_amount_list, self.user_data.contract_demand,
                                self.user_data.class1, self.user_data.class2, self.user_data.class_contract)
            print(int(calc.init_calc_month(month - 1)))
            result = calc.init_calc_month(month - 1)
        else:
            print("잘못된 입력입니다.")
            result = 0.0

        return result
