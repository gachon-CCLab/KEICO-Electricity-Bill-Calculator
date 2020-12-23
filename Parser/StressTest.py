from calc_Charge.Parser.KEPCO_Parser import *
from calc_Charge.CalcHome import *
from calc_Charge.CalcGeneral import *
from calc_Charge.CalcIndustry import *
import random

# #####TEST-HOME###############################################################
# used_amount_list_home: list[int] = [0 for i in range(12)]
# used_amount_list_home[0] = 1204      # 1월 사용량
# used_amount_list_home[1] = 1203
# used_amount_list_home[2] = 1202
# used_amount_list_home[3] = 1201
# used_amount_list_home[4] = 1111
# used_amount_list_home[5] = 1123
# used_amount_list_home[6] = 1213
# used_amount_list_home[7] = 1521
# used_amount_list_home[8] = 1234
# used_amount_list_home[9] = 1123
# used_amount_list_home[10] = 1423
# used_amount_list_home[11] = 1204
# print(used_amount_list_home)
# #############################################################################
#
# #####TEST-General###############################################################
# used_amount_list_general = [[0 for i in range(3)] for j in range(12)]
# used_amount_list_general[0] = [1, 1, 1]      # 1월 사용량   # 계약전력으로 구분되지 않을 경우 index [0]에 사용량.
# used_amount_list_general[1] = [1, 1, 1]
# used_amount_list_general[2] = [1, 1, 1]
# used_amount_list_general[3] = [1, 1, 1]
# used_amount_list_general[4] = [1, 1, 1]
# used_amount_list_general[5] = [1, 1, 1]
# used_amount_list_general[6] = [1, 1, 1]
# used_amount_list_general[7] = [5, 300, 20]
# used_amount_list_general[8] = [1, 1, 1]
# used_amount_list_general[9] = [1, 1, 1]
# used_amount_list_general[10] = [1, 1, 1]
# used_amount_list_general[11] = [1, 1, 1]
# contract_demand = 10
# class1 = 0
# class2 = 1
# class_contract = 0
# print(used_amount_list_general)
# #############################################################################
#
# #####TEST-Industry###############################################################
# used_amount_list_industry = [[0 for i in range(3)] for j in range(12)]
# used_amount_list_industry[0] = [1, 1, 1]  # 1월 사용량   # 계약전력으로 구분되지 않을 경우 index [0]에 사용량.
# used_amount_list_industry[1] = [1, 1, 1]
# used_amount_list_industry[2] = [1, 1, 1]
# used_amount_list_industry[3] = [1, 1, 1]
# used_amount_list_industry[4] = [1, 1, 1]
# used_amount_list_industry[5] = [1, 1, 1]
# used_amount_list_industry[6] = [1, 1, 1]
# used_amount_list_industry[7] = [5, 300, 20]
# used_amount_list_industry[8] = [1, 1, 1]
# used_amount_list_industry[9] = [1, 1, 1]
# used_amount_list_industry[10] = [1, 1, 1]
# used_amount_list_industry[11] = [1, 1, 1]
# # contract_demand = 10
# # class1 = 0
# # class2 = 0
# # class_contract = 0
# # print(used_amount_list_industry)
# #############################################################################
#
# # a = Parser(1, used_amount_list_home, 0, 0, 0, 0)
# # result: int = a.init_calc()
# # print(result)

used_amount_list_home: list[int] = [0 for i in range(12)]
used_amount_list_general = [[0 for i in range(3)] for j in range(12)]   # 2차원 배열 초기화
used_amount_list_industry = [[0 for i in range(3)] for j in range(12)]  # 2차원 배열 초기화

success_count: int = 0
failure_count: int = 0

for i in range(100):
    contract_demand: int  # 계약 전력(kWh)  # 4kWh 이상?
    charge: float = 0

    voltage_factor: int = 0  # 0: 저압, 1: 고압 (in home Calc)

    # 0: 갑I, 1: 갑II, 2: 을
    class1: int = 0

    # 갑I  -> 0: 저압,  1: 고압A, 2: 고압B
    # 갑II -> 0: 고압A, 1: 고압B
    # 을   -> 0: 고압A, 1: 고압B, 2: 고압C
    class2: int = 0

    # 0: 선택I(or 한가지 경우 default), 1: 선택II, 2: 선택III
    class_contract: int = 0

    # 0: 주택용(저압), 1: 주택용(고압), 2: 일반용(갑)I, 3: 일반용(갑)II
    # 4: 일반용(을),  5: 산업용(갑)I,  6: 산업용(갑)II, 7: 산업용(을)
    selector: int

    selector = random.randint(0, 7)
    contract_demand = random.randint(5, 100)

    # 제작 코드의 객체 설정
    if selector == 0:
        voltage_factor = 0
    elif selector == 1:
        voltage_factor = 1
    elif selector == 2 or selector == 5:
        class1 = 0
        class2 = random.randint(0, 2)
        if class2 == 1 or class2 == 2:
            class_contract = random.randint(0, 1)
    elif selector == 3 or selector == 6:
        class1 = 1
        class2 = random.randint(0, 1)
        class_contranct = random.randint(0, 1)
    elif selector == 4 or selector == 7:
        class1 = 2
        class2 = random.randint(0, 2)
        class_contract = random.randint(0, 2)
    else:
        print("X")

    if 0 <= selector <= 1:
        used_amount_list_home = [random.randint(0, 2000) for i in range(12)]
        MyCalc = CalcHome(used_amount_list_home, voltage_factor)
        KEPCO_Parser = Parser(selector, used_amount_list_home, contract_demand, class1, class2, class_contract)
    elif 2 <= selector <= 4:
        used_amount_list_general = [[random.randint(0, 2000) for i in range(3)] for j in range(12)]  # 2차원 배열 초기화
        MyCalc = CalcGeneral(used_amount_list_general, contract_demand, class1, class2, class_contract)
        KEPCO_Parser = Parser(selector, used_amount_list_general, contract_demand, class1, class2, class_contract)
    elif 5 <= selector <= 7:
        used_amount_list_industry = [[random.randint(0, 2000) for i in range(3)] for j in range(12)]  # 2차원 배열 초기화
        MyCalc = CalcIndustry(used_amount_list_industry, contract_demand, class1, class2, class_contract)
        KEPCO_Parser = Parser(selector, used_amount_list_industry, contract_demand, class1, class2, class_contract)
    else:
        print("X")

    # noinspection PyUnboundLocalVariable
    MyCalc_result = int(MyCalc.init_calc())
    print(MyCalc_result)

    KEPCO_result: int = KEPCO_Parser.init_calc()
    print(KEPCO_result)

    print('selector :', selector)
    print('class2 :', class2)
    print('class_contract :', class_contract)
    print('contract_demand :', contract_demand)
    print(used_amount_list_home)
    print(used_amount_list_general)
    print(used_amount_list_industry)
    if MyCalc_result == KEPCO_result:
        print(str(i+1) + "번째 try 성공")
        success_count += 1
    else:
        print(str(i+1) + "번째 try 실패")
        failure_count += 1

    print("성공 : " + str(success_count) + ", 실패 : " + str(failure_count))




