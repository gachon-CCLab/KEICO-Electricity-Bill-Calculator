from calc_Charge.CalcCharge import *


class CalcGeneral(CalcCharge):
    def __init__(self, used_amount_list_, contract_demand, class1, class2, class_contract):
        self.used_amount_list = used_amount_list_
        self.contract_demand = contract_demand
        self.class1 = class1
        self.class2 = class2
        self.class_contract = class_contract

    def init_calc(self):
        charge: float = 0

        for i in range(12):
            summer: bool = 0  # 여름
            winter: bool = 0  # 겨울
            if self.used_amount_list[i] != [0, 0, 0]:
                if self.class1 == 0:
                    if 6 <= i <= 7:
                        summer = 1
                    elif (0 <= i <= 1) or i == 11:
                        winter = 1
                elif self.class1 == 1 or self.class1 == 2:
                    if 5 <= i <= 7:
                        summer = 1
                    elif (0 <= i <= 1) or (10 <= i <= 11):
                        winter = 1
                charge += self.calc(i, self.class1, self.class2, self.class_contract, summer, winter)

        return charge

    # 갑I에만 '여름철', '겨울철' <==> 갑II, 을: '여름', '겨울' 구분 주의
    def calc(self, i, class1, class2, class_contract, summer, winter):
        used_amount = self.used_amount_list[i]
        charge_: int = 0
        if class1 == 0:
            used_amount = used_amount[0]
            if class2 == 0:                 # 갑I - 저압
                if summer == 1:
                    charge_ = 6160 * self.contract_demand + 105.7 * used_amount
                elif winter == 1:
                    charge_ = 6160 * self.contract_demand + 92.3 * used_amount
                else:
                    charge_ = 6160 * self.contract_demand + 65.2 * used_amount
            elif class2 == 1:
                if class_contract == 0:     # 갑I - 고압A - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + 115.9 * used_amount
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + 103.6 * used_amount
                    else:
                        charge_ = 7170 * self.contract_demand + 71.9 * used_amount
                elif class_contract == 1:   # 갑I - 고압A - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + 111.9 * used_amount
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + 98.3 * used_amount
                    else:
                        charge_ = 8230 * self.contract_demand + 67.6 * used_amount
                else:
                    print("Wrong input")
            elif class2 == 2:
                if class_contract == 0:     # 갑I - 고압B - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + 113.8 * used_amount
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + 100.6 * used_amount
                    else:
                        charge_ = 7170 * self.contract_demand + 70.8 * used_amount
                elif class_contract == 1:   # 갑I - 고압B - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + 108.5 * used_amount
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + 95.3 * used_amount
                    else:
                        charge_ = 8230 * self.contract_demand + 65.5 * used_amount
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        elif class1 == 1:
            if class2 == 0:
                if class_contract == 0:     # 갑II - 고압A - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + 62.7 * used_amount[0] + 113.9 * used_amount[1] \
                                  + 136.4 * used_amount[2]
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + 71.4 * used_amount[0] + 101.8 * used_amount[1] \
                                  + 116.6 * used_amount[2]
                    else:
                        charge_ = 7170 * self.contract_demand + 62.7 * used_amount[0] + 70.1 * used_amount[1] \
                                  + 81.4 * used_amount[2]
                elif class_contract == 1:   # 갑II - 고압A - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + 57.4 * used_amount[0] + 108.6 * used_amount[1] \
                                  + 131.1 * used_amount[2]
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + 66.1 * used_amount[0] + 96.5 * used_amount[1] \
                                  + 111.3 * used_amount[2]
                    else:
                        charge_ = 8230 * self.contract_demand + 57.4 * used_amount[0] + 64.8 * used_amount[1] \
                                  + 76.1 * used_amount[2]
                else:
                    print("Wrong input")
            elif class2 == 1:
                if class_contract == 0:     # 갑II - 고압B - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + 62.1 * used_amount[0] + 110.7 * used_amount[1] \
                                  + 127.1 * used_amount[2]
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + 71.1 * used_amount[0] + 98.4 * used_amount[1] \
                                  + 112.6 * used_amount[2]
                    else:
                        charge_ = 7170 * self.contract_demand + 62.1 * used_amount[0] + 68.0 * used_amount[1] \
                                  + 73.4 * used_amount[2]
                elif class_contract == 1:   # 갑II - 고압B - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + 56.8 * used_amount[0] + 105.4 * used_amount[1] \
                                  + 121.8 * used_amount[2]
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + 65.8 * used_amount[0] + 93.1 * used_amount[1] \
                                  + 107.3 * used_amount[2]
                    else:
                        charge_ = 8230 * self.contract_demand + 56.8 * used_amount[0] + 62.7 * used_amount[1] \
                                  + 68.1 * used_amount[2]
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        elif class1 == 2:
            if class2 == 0:
                if class_contract == 0:     # 을 - 고압A - 계약I
                    if summer == 1:
                        charge_ = 7220 * self.contract_demand + 61.6 * used_amount[0] + 114.5 * used_amount[1] \
                                  + 196.6 * used_amount[2]
                    elif winter == 1:
                        charge_ = 7220 * self.contract_demand + 68.6 * used_amount[0] + 114.7 * used_amount[1] \
                                  + 172.2 * used_amount[2]
                    else:
                        charge_ = 7220 * self.contract_demand + 61.6 * used_amount[0] + 84.1 * used_amount[1] \
                                  + 114.8 * used_amount[2]
                elif class_contract == 1:   # 을 - 고압A - 계약II
                    if summer == 1:
                        charge_ = 8320 * self.contract_demand + 56.1 * used_amount[0] + 109.0 * used_amount[1] \
                                  + 191.1 * used_amount[2]
                    elif winter == 1:
                        charge_ = 8320 * self.contract_demand + 63.1 * used_amount[0] + 109.2 * used_amount[1] \
                                  + 166.7 * used_amount[2]
                    else:
                        charge_ = 8320 * self.contract_demand + 56.1 * used_amount[0] + 78.6 * used_amount[1] \
                                  + 109.3 * used_amount[2]
                elif class_contract == 2:   # 을 - 고압A - 계약III
                    if summer == 1:
                        charge_ = 9810 * self.contract_demand + 55.2 * used_amount[0] + 108.4 * used_amount[1] \
                                  + 178.7 * used_amount[2]
                    elif winter == 1:
                        charge_ = 9810 * self.contract_demand + 62.5 * used_amount[0] + 108.6 * used_amount[1] \
                                  + 155.5 * used_amount[2]
                    else:
                        charge_ = 9810 * self.contract_demand + 55.2 * used_amount[0] + 77.3 * used_amount[1] \
                                  + 101.0 * used_amount[2]
                else:
                    print("Wrong input")
            elif class2 == 1:
                if class_contract == 0:     # 을 - 고압B - 계약I
                    if summer == 1:
                        charge_ = 6630 * self.contract_demand + 60.0 * used_amount[0] + 112.3 * used_amount[1] \
                                  + 193.5 * used_amount[2]
                    elif winter == 1:
                        charge_ = 6630 * self.contract_demand + 67.0 * used_amount[0] + 112.3 * used_amount[1] \
                                  + 168.5 * used_amount[2]
                    else:
                        charge_ = 6630 * self.contract_demand + 60.0 * used_amount[0] + 82.3 * used_amount[1] \
                                  + 112.6 * used_amount[2]
                elif class_contract == 1:   # 을 - 고압B - 계약II
                    if summer == 1:
                        charge_ = 7380 * self.contract_demand + 56.2 * used_amount[0] + 108.5 * used_amount[1] \
                                  + 189.7 * used_amount[2]
                    elif winter == 1:
                        charge_ = 7380 * self.contract_demand + 63.2 * used_amount[0] + 108.5 * used_amount[1] \
                                  + 164.7 * used_amount[2]
                    else:
                        charge_ = 7380 * self.contract_demand + 56.2 * used_amount[0] + 78.5 * used_amount[1] \
                                  + 108.8 * used_amount[2]
                elif class_contract == 2:   # 을 - 고압B - 계약III
                    if summer == 1:
                        charge_ = 8190 * self.contract_demand + 54.5 * used_amount[0] + 106.8 * used_amount[1] \
                                  + 188.1 * used_amount[2]
                    elif winter == 1:
                        charge_ = 8190 * self.contract_demand + 61.6 * used_amount[0] + 106.8 * used_amount[1] \
                                  + 163.0 * used_amount[2]
                    else:
                        charge_ = 8190 * self.contract_demand + 54.5 * used_amount[0] + 76.9 * used_amount[1] \
                                  + 107.2 * used_amount[2]
                else:
                    print("Wrong input")
            elif class2 == 2:
                if class_contract == 0:     # 을 - 고압C - 계약I
                    if summer == 1:
                        charge_ = 6590 * self.contract_demand + 59.5 * used_amount[0] + 112.4 * used_amount[1] \
                                  + 193.3 * used_amount[2]
                    elif winter == 1:
                        charge_ = 6590 * self.contract_demand + 66.4 * used_amount[0] + 112.0 * used_amount[1] \
                                  + 168.6 * used_amount[2]
                    else:
                        charge_ = 6590 * self.contract_demand + 59.5 * used_amount[0] + 82.4 * used_amount[1] \
                                  + 112.8 * used_amount[2]
                elif class_contract == 1:   # 을 - 고압C - 계약II
                    if summer == 1:
                        charge_ = 7520 * self.contract_demand + 54.8 * used_amount[0] + 107.7 * used_amount[1] \
                                  + 188.6 * used_amount[2]
                    elif winter == 1:
                        charge_ = 7520 * self.contract_demand + 61.7 * used_amount[0] + 107.3 * used_amount[1] \
                                  + 163.9 * used_amount[2]
                    else:
                        charge_ = 7520 * self.contract_demand + 54.8 * used_amount[0] + 77.7 * used_amount[1] \
                                  + 108.1 * used_amount[2]
                elif class_contract == 2:   # 을 - 고압C - 계약III
                    if summer == 1:
                        charge_ = 8090 * self.contract_demand + 53.7 * used_amount[0] + 106.6 * used_amount[1] \
                                  + 187.5 * used_amount[2]
                    elif winter == 1:
                        charge_ = 8090 * self.contract_demand + 60.6 * used_amount[0] + 106.2 * used_amount[1] \
                                  + 162.8 * used_amount[2]
                    else:
                        charge_ = 8090 * self.contract_demand + 53.7 * used_amount[0] + 76.6 * used_amount[1] \
                                  + 107.0 * used_amount[2]
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        else:
            print("Wrong input")

        return charge_      # 부가가치세, 전력산업기반기금, 필수 사용량 보장공제 제외.

