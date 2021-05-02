from CalcHome import *
from CalcGeneral import *
from CalcIndustry import *  # 일반용, 산업용 요금 유사.   # 일반용 을 == 산업용 을

if __name__ == '__main__':

    # 들어오는 데이터에 따라 분기
    used_amount_list_home: list[int] = [0 for i in range(12)]
    used_amount_list_general = [[0 for i in range(3)] for j in range(12)]   # 2차원 배열 초기화
    used_amount_list_industry = [[0 for i in range(3)] for j in range(12)]  # 2차원 배열 초기화

    contract_demand: int = 0   # 계약 전력(kWh)  # 4kWh 이상?
    charge: float = 0

    voltage_factor = 0  # 0: 저압, 1: 고압 (in home Calc)

    # 0: 갑I, 1: 갑II, 2: 을
    class1: int = 0

    # 갑I  -> 0: 저압,  1: 고압A, 2: 고압B
    # 갑II -> 0: 고압A, 1: 고압B
    # 을   -> 0: 고압A, 1: 고압B, 2: 고압C
    class2: int = 0

    # 0: 선택I(or 한가지 경우 default), 1: 선택II, 2: 선택III
    class_contract: int = 0

    #####TEST-HOME###############################################################
    used_amount_list_home[0] = 1204  # 1월 사용량
    used_amount_list_home[1] = 1203
    used_amount_list_home[2] = 1202
    used_amount_list_home[3] = 1201
    used_amount_list_home[4] = 1111
    used_amount_list_home[5] = 1123
    used_amount_list_home[6] = 1213
    used_amount_list_home[7] = 1521
    used_amount_list_home[8] = 1234
    used_amount_list_home[9] = 1123
    used_amount_list_home[10] = 1423
    used_amount_list_home[11] = 1204
    voltage_factor = 0
    # print(used_amount_list_home)
    #############################################################################

    #####TEST-General###############################################################
    used_amount_list_general[0] = [1, 1, 1]      # 1월 사용량   # 계약전력으로 구분되지 않을 경우 index [0]에 사용량.
    used_amount_list_general[1] = [1, 1, 1]
    used_amount_list_general[2] = [1, 1, 1]
    used_amount_list_general[3] = [1, 1, 1]
    used_amount_list_general[4] = [1, 1, 1]
    used_amount_list_general[5] = [1, 1, 1]
    used_amount_list_general[6] = [1, 1, 1]
    used_amount_list_general[7] = [5, 300, 20]
    used_amount_list_general[8] = [1, 1, 1]
    used_amount_list_general[9] = [1, 1, 1]
    used_amount_list_general[10] = [1, 1, 1]
    used_amount_list_general[11] = [1, 1, 1]
    contract_demand = 10
    class1 = 0
    class2 = 0
    class_contract = 0
    # print(used_amount_list_general)
    #############################################################################

    #####TEST-Industry###############################################################
    used_amount_list_industry[0] = [1, 1, 1]      # 1월 사용량   # 계약전력으로 구분되지 않을 경우 index [0]에 사용량.
    used_amount_list_industry[1] = [1, 1, 1]
    used_amount_list_industry[2] = [1, 1, 1]
    used_amount_list_industry[3] = [1, 1, 1]
    used_amount_list_industry[4] = [1, 1, 1]
    used_amount_list_industry[5] = [1, 1, 1]
    used_amount_list_industry[6] = [1, 1, 1]
    used_amount_list_industry[7] = [5, 300, 20]
    used_amount_list_industry[8] = [1, 1, 1]
    used_amount_list_industry[9] = [1, 1, 1]
    used_amount_list_industry[10] = [1, 1, 1]
    used_amount_list_industry[11] = [1, 1, 1]
    contract_demand = 51
    class1 = 1
    class2 = 1
    class_contract = 0
    # print(used_amount_list_industry)
    #############################################################################

    used_amount_list_home = [192, 1483, 1360, 741, 938, 943, 1954, 294, 1353, 216, 1543, 1346]
    used_amount_list_general = [[1278, 1894, 551], [1844, 31, 78], [767, 761, 1650], [1365, 1862, 1228], [1959, 1826, 816], [524, 531, 494], [174, 1407, 1402], [849, 658, 1918], [898, 1045, 705], [1327, 79, 1181], [1460, 756, 805], [1022, 1775, 1950]]
    #############################################################################
    a = CalcHome(used_amount_list_home, voltage_factor)
    a_result = int(a.init_calc())
    print("청구금액 :", a_result)

    b = CalcGeneral(used_amount_list_general, contract_demand, class1, class2, class_contract)
    b_result = int(b.init_calc())  # 전기요금계(기본요금 + 전력량요금)
    print("청구금액 :", b_result)

    # c = CalcIndustry(used_amount_list_industry, contract_demand, class1, class2, class_contract)
    # # 전기요금계(기본요금 + 전력량요금)
    # # 부가가치세  # 사사오입
    # # 전련산업기반기금  # 10원미만 절사
    # print("청구금액 :", c_result)
    #############################################################################
    # 전기요금계(기본요금 + 전력량요금)
    # 부가가치세  # 사사오입
    # 전련산업기반기금  # 10원미만 절사
