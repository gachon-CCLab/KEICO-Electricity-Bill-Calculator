class CalcIndustry:
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
                    charge_ = 5550 * self.contract_demand + 81.0 * used_amount
                elif winter == 1:
                    charge_ = 5550 * self.contract_demand + 79.3 * used_amount
                else:
                    charge_ = 5550 * self.contract_demand + 59.2 * used_amount
            elif class2 == 1:
                if class_contract == 0:     # 갑I - 고압A - 계약I
                    if summer == 1:
                        charge_ = 6490 * self.contract_demand + 89.6 * used_amount
                    elif winter == 1:
                        charge_ = 6490 * self.contract_demand + 89.5 * used_amount
                    else:
                        charge_ = 6490 * self.contract_demand + 65.9 * used_amount
                elif class_contract == 1:   # 갑I - 고압A - 계약II
                    if summer == 1:
                        charge_ = 7470 * self.contract_demand + 84.8 * used_amount
                    elif winter == 1:
                        charge_ = 7470 * self.contract_demand + 83.0 * used_amount
                    else:
                        charge_ = 7470 * self.contract_demand + 61.3 * used_amount
                else:
                    print("Wrong input")
            elif class2 == 2:
                if class_contract == 0:     # 갑I - 고압B - 계약I
                    if summer == 1:
                        charge_ = 6000 * self.contract_demand + 88.4 * used_amount
                    elif winter == 1:
                        charge_ = 6000 * self.contract_demand + 88.0 * used_amount
                    else:
                        charge_ = 6000 * self.contract_demand + 64.8 * used_amount
                elif class_contract == 1:   # 갑I - 고압B - 계약II
                    if summer == 1:
                        charge_ = 6900 * self.contract_demand + 83.7 * used_amount
                    elif winter == 1:
                        charge_ = 6900 * self.contract_demand + 81.9 * used_amount
                    else:
                        charge_ = 6900 * self.contract_demand + 60.2 * used_amount
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        elif class1 == 1:
            if class2 == 0:
                if class_contract == 0:     # 갑II - 고압A - 계약I
                    if summer == 1:
                        charge_ = 6490 * self.contract_demand + 60.5 * used_amount[0] + 86.3 * used_amount[1] \
                                  + 119.8 * used_amount[2]
                    elif winter == 1:
                        charge_ = 6490 * self.contract_demand + 67.9 * used_amount[0] + 84.8 * used_amount[1] \
                                  + 114.2 * used_amount[2]
                    else:
                        charge_ = 6490 * self.contract_demand + 60.5 * used_amount[0] + 65.3 * used_amount[1] \
                                  + 84.5 * used_amount[2]
                elif class_contract == 1:   # 갑II - 고압A - 계약II
                    if summer == 1:
                        charge_ = 7470 * self.contract_demand + 55.6 * used_amount[0] + 81.4 * used_amount[1] \
                                  + 114.9 * used_amount[2]
                    elif winter == 1:
                        charge_ = 7470 * self.contract_demand + 63.0 * used_amount[0] + 79.9 * used_amount[1] \
                                  + 109.3 * used_amount[2]
                    else:
                        charge_ = 7470 * self.contract_demand + 55.6 * used_amount[0] + 60.4 * used_amount[1] \
                                  + 79.6 * used_amount[2]
                else:
                    print("Wrong input")
            elif class2 == 1:
                if class_contract == 0:     # 갑II - 고압B - 계약I
                    if summer == 1:
                        charge_ = 6000 * self.contract_demand + 57.3 * used_amount[0] + 84.9 * used_amount[1] \
                                  + 118.7 * used_amount[2]
                    elif winter == 1:
                        charge_ = 6000 * self.contract_demand + 64.5 * used_amount[0] + 82.5 * used_amount[1] \
                                  + 111.2 * used_amount[2]
                    else:
                        charge_ = 6000 * self.contract_demand + 57.3 * used_amount[0] + 63.9 * used_amount[1] \
                                  + 82.7 * used_amount[2]
                elif class_contract == 1:   # 갑II - 고압B - 계약II
                    if summer == 1:
                        charge_ = 6900 * self.contract_demand + 52.8 * used_amount[0] + 80.4 * used_amount[1] \
                                  + 114.2 * used_amount[2]
                    elif winter == 1:
                        charge_ = 6900 * self.contract_demand + 60.0 * used_amount[0] + 78.0 * used_amount[1] \
                                  + 106.7 * used_amount[2]
                    else:
                        charge_ = 6900 * self.contract_demand + 52.8 * used_amount[0] + 59.4 * used_amount[1] \
                                  + 78.2 * used_amount[2]
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
