from CalcCharge import *


class CalcGeneral(CalcCharge):
    def __init__(self, used_amount_list_, contract_demand, class1, class2, class_contract):
        self.used_amount_list = used_amount_list_
        self.contract_demand = contract_demand
        self.class1 = class1
        self.class2 = class2
        self.class_contract = class_contract

    @staticmethod
    def get_precise(num):  # int()의 역할(즉, 내림(절삭)) + 부동소수점 오류 fix
        if (num - int(num)) != 0.5:
            if abs(round(num) - num) <= 0.01:
                num = round(num)
        return int(num)

    def init_calc(self):
        charge: float = 0
        tmp_charge: float
        env_contribution, fuel_rate = CalcCharge.get_conf(self)

        for i in range(12):
            summer: bool = 0  # 여름
            winter: bool = 0  # 겨울
            if self.used_amount_list[i] != [0, 0, 0]:   # v
                if 5 <= i <= 7:
                    summer = 1
                elif (0 <= i <= 1) or (10 <= i <= 11):
                    winter = 1
                tmp_charge = self.calc(i, self.class1, self.class2, self.class_contract, summer, winter)
                result = self.get_precise(tmp_charge)  # 전기요금계(기본요금 + 전력량요금)

                # 일반용은 사용량 0일 시 50% 감면
                if (self.class1 == 0 and self.used_amount_list[i][0] == 0) or (self.used_amount_list == [0, 0, 0]):
                    result = self.get_precise(result / 2)

                # 총 사용량 구하기
                if self.class1 != 0:        # 갑 I 이 아니면,
                    used_sum = self.used_amount_list[i][0] + self.used_amount_list[i][1] + self.used_amount_list[i][2]
                else:
                    used_sum = self.used_amount_list[i][0]
                result = self.get_precise(result + used_sum * env_contribution)   # 환경부담금
                result = self.get_precise(result + used_sum * fuel_rate)          # 연료비조정액

                tax1 = result * 0.1  # 부가가치세  # 사사오입
                if (tax1 - self.get_precise(tax1)) >= 0.5:
                    tax1 = self.get_precise(tax1) + 1
                else:
                    tax1 = self.get_precise(tax1)
                tax2 = self.get_precise((result * 0.037) - ((result * 0.037) % 10))  # 전련산업기반기금  # 10원미만 절사
                tmp_charge = result + tax1 + tax2
                tmp_charge = tmp_charge - (tmp_charge % 10)
                print(str(i+1) + "월 요금")
                print("전기 요금계 :", result)
                print("부가가치세 :", tax1)
                print("전력산업기반기금 :", tax2)
                print("청구금액 :", tmp_charge, "\n")
                charge += tmp_charge

        return charge

    def init_calc_month(self, i):
        charge: float = 0
        tmp_charge: float
        env_contribution, fuel_rate = CalcCharge.get_conf(self)


        summer: bool = 0  # 여름
        winter: bool = 0  # 겨울
        if self.used_amount_list[i] != [0, 0, 0]:   # v
            if 5 <= i <= 7:
                summer = 1
            elif (0 <= i <= 1) or (10 <= i <= 11):
                winter = 1
            tmp_charge = self.calc(i, self.class1, self.class2, self.class_contract, summer, winter)
            result = self.get_precise(tmp_charge)  # 전기요금계(기본요금 + 전력량요금)

            # 일반용은 사용량 0일 시 50% 감면
            if (self.class1 == 0 and self.used_amount_list[i][0] == 0) or (self.used_amount_list == [0, 0, 0]):
                result = self.get_precise(result / 2)

            # 총 사용량 구하기
            if self.class1 != 0:        # 갑 I 이 아니면,
                used_sum = self.used_amount_list[i][0] + self.used_amount_list[i][1] + self.used_amount_list[i][2]
            else:
                used_sum = self.used_amount_list[i][0]
            result = self.get_precise(result + used_sum * env_contribution)   # 환경부담금
            result = self.get_precise(result + used_sum * fuel_rate)          # 연료비조정액

            tax1 = result * 0.1  # 부가가치세  # 사사오입
            if (tax1 - self.get_precise(tax1)) >= 0.5:
                tax1 = self.get_precise(tax1) + 1
            else:
                tax1 = self.get_precise(tax1)
            tax2 = self.get_precise((result * 0.037) - ((result * 0.037) % 10))  # 전련산업기반기금  # 10원미만 절사
            tmp_charge = result + tax1 + tax2
            tmp_charge = tmp_charge - (tmp_charge % 10)
            print(str(i+1) + "월 요금")
            print("전기 요금계 :", result)
            print("부가가치세 :", tax1)
            print("전력산업기반기금 :", tax2)
            print("청구금액 :", tmp_charge, "\n")
            charge += tmp_charge

        return charge

    # .
    def calc(self, i, class1, class2, class_contract, summer, winter):
        used_amount = self.used_amount_list[i]
        charge_: int = 0
        if class1 == 0:
            used_amount = used_amount[0]
            if class2 == 0:                 # 갑I - 저압
                if summer == 1:
                    charge_ = 6160 * self.contract_demand + self.get_precise(105.7 * used_amount)
                elif winter == 1:
                    charge_ = 6160 * self.contract_demand + self.get_precise(92.3 * used_amount)
                else:
                    charge_ = 6160 * self.contract_demand + self.get_precise(65.2 * used_amount)
            elif class2 == 1:
                if class_contract == 0:     # 갑I - 고압A - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(115.9 * used_amount)
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(103.6 * used_amount)
                    else:
                        charge_ = 7170 * self.contract_demand + self.get_precise(71.9 * used_amount)
                elif class_contract == 1:   # 갑I - 고압A - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(111.9 * used_amount)
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(98.3 * used_amount)
                    else:
                        charge_ = 8230 * self.contract_demand + self.get_precise(67.6 * used_amount)
                else:
                    print("Wrong input")
            elif class2 == 2:
                if class_contract == 0:     # 갑I - 고압B - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(113.8 * used_amount)
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(100.6 * used_amount)
                    else:
                        charge_ = 7170 * self.contract_demand + self.get_precise(70.8 * used_amount)
                elif class_contract == 1:   # 갑I - 고압B - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(108.5 * used_amount)
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(95.3 * used_amount)
                    else:
                        charge_ = 8230 * self.contract_demand + self.get_precise(65.5 * used_amount)
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        elif class1 == 1:
            if class2 == 0:
                if class_contract == 0:     # 갑II - 고압A - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(62.7 * used_amount[0]) + self.get_precise(113.9 * used_amount[1]) \
                                  + self.get_precise(136.4 * used_amount[2])
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(71.4 * used_amount[0]) + self.get_precise(101.8 * used_amount[1]) \
                                  + self.get_precise(116.6 * used_amount[2])
                    else:
                        charge_ = 7170 * self.contract_demand + self.get_precise(62.7 * used_amount[0]) + self.get_precise(70.1 * used_amount[1]) \
                                  + self.get_precise(81.4 * used_amount[2])
                elif class_contract == 1:   # 갑II - 고압A - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(57.4 * used_amount[0]) + self.get_precise(108.6 * used_amount[1]) \
                                  + self.get_precise(131.1 * used_amount[2])
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(66.1 * used_amount[0]) + self.get_precise(96.5 * used_amount[1]) \
                                  + self.get_precise(111.3 * used_amount[2])
                    else:
                        charge_ = 8230 * self.contract_demand + self.get_precise(57.4 * used_amount[0]) + self.get_precise(64.8 * used_amount[1]) \
                                  + self.get_precise(76.1 * used_amount[2])
                else:
                    print("Wrong input")
            elif class2 == 1:
                if class_contract == 0:     # 갑II - 고압B - 계약I
                    if summer == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(62.1 * used_amount[0]) + self.get_precise(110.7 * used_amount[1]) \
                                  + self.get_precise(127.1 * used_amount[2])
                    elif winter == 1:
                        charge_ = 7170 * self.contract_demand + self.get_precise(71.1 * used_amount[0]) + self.get_precise(98.4 * used_amount[1]) \
                                  + self.get_precise(112.6 * used_amount[2])
                    else:
                        charge_ = 7170 * self.contract_demand + self.get_precise(62.1 * used_amount[0]) + self.get_precise(68.0 * used_amount[1]) \
                                  + self.get_precise(73.4 * used_amount[2])
                elif class_contract == 1:   # 갑II - 고압B - 계약II
                    if summer == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(56.8 * used_amount[0]) + self.get_precise(105.4 * used_amount[1]) \
                                  + self.get_precise(121.8 * used_amount[2])
                    elif winter == 1:
                        charge_ = 8230 * self.contract_demand + self.get_precise(65.8 * used_amount[0]) + self.get_precise(93.1 * used_amount[1]) \
                                  + self.get_precise(107.3 * used_amount[2])
                    else:
                        charge_ = 8230 * self.contract_demand + self.get_precise(56.8 * used_amount[0]) + self.get_precise(62.7 * used_amount[1]) \
                                  + self.get_precise(68.1 * used_amount[2])
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        elif class1 == 2:
            if class2 == 0:
                if class_contract == 0:     # 을 - 고압A - 계약I
                    if summer == 1:
                        charge_ = 7220 * self.contract_demand + self.get_precise(61.6 * used_amount[0]) + self.get_precise(114.5 * used_amount[1]) \
                                  + self.get_precise(196.6 * used_amount[2])
                    elif winter == 1:
                        charge_ = 7220 * self.contract_demand + self.get_precise(68.6 * used_amount[0]) + self.get_precise(114.7 * used_amount[1]) \
                                  + self.get_precise(172.2 * used_amount[2])
                    else:
                        charge_ = 7220 * self.contract_demand + self.get_precise(61.6 * used_amount[0]) + self.get_precise(84.1 * used_amount[1]) \
                                  + self.get_precise(114.8 * used_amount[2])
                elif class_contract == 1:   # 을 - 고압A - 계약II
                    if summer == 1:
                        charge_ = 8320 * self.contract_demand + self.get_precise(56.1 * used_amount[0]) + self.get_precise(109.0 * used_amount[1]) \
                                  + self.get_precise(191.1 * used_amount[2])
                    elif winter == 1:
                        charge_ = 8320 * self.contract_demand + self.get_precise(63.1 * used_amount[0]) + self.get_precise(109.2 * used_amount[1]) \
                                  + self.get_precise(166.7 * used_amount[2])
                    else:
                        charge_ = 8320 * self.contract_demand + self.get_precise(56.1 * used_amount[0]) + self.get_precise(78.6 * used_amount[1]) \
                                  + self.get_precise(109.3 * used_amount[2])
                elif class_contract == 2:   # 을 - 고압A - 계약III
                    if summer == 1:
                        charge_ = 9810 * self.contract_demand + self.get_precise(55.2 * used_amount[0]) + self.get_precise(108.4 * used_amount[1]) \
                                  + self.get_precise(178.7 * used_amount[2])
                    elif winter == 1:
                        charge_ = 9810 * self.contract_demand + self.get_precise(62.5 * used_amount[0]) + self.get_precise(108.6 * used_amount[1]) \
                                  + self.get_precise(155.5 * used_amount[2])
                    else:
                        charge_ = 9810 * self.contract_demand + self.get_precise(55.2 * used_amount[0]) + self.get_precise(77.3 * used_amount[1]) \
                                  + self.get_precise(101.0 * used_amount[2])
                else:
                    print("Wrong input")
            elif class2 == 1:
                if class_contract == 0:     # 을 - 고압B - 계약I
                    if summer == 1:
                        charge_ = 6630 * self.contract_demand + self.get_precise(60.0 * used_amount[0]) + self.get_precise(112.3 * used_amount[1]) \
                                  + self.get_precise(193.5 * used_amount[2])
                    elif winter == 1:
                        charge_ = 6630 * self.contract_demand + self.get_precise(67.0 * used_amount[0]) + self.get_precise(112.3 * used_amount[1]) \
                                  + self.get_precise(168.5 * used_amount[2])
                    else:
                        charge_ = 6630 * self.contract_demand + self.get_precise(60.0 * used_amount[0]) + self.get_precise(82.3 * used_amount[1]) \
                                  + self.get_precise(112.6 * used_amount[2])
                elif class_contract == 1:   # 을 - 고압B - 계약II
                    if summer == 1:
                        charge_ = 7380 * self.contract_demand + self.get_precise(56.2 * used_amount[0]) + self.get_precise(108.5 * used_amount[1]) \
                                  + self.get_precise(189.7 * used_amount[2])
                    elif winter == 1:
                        charge_ = 7380 * self.contract_demand + self.get_precise(63.2 * used_amount[0]) + self.get_precise(108.5 * used_amount[1]) \
                                  + self.get_precise(164.7 * used_amount[2])
                    else:
                        charge_ = 7380 * self.contract_demand + self.get_precise(56.2 * used_amount[0]) + self.get_precise(78.5 * used_amount[1]) \
                                  + self.get_precise(108.8 * used_amount[2])
                elif class_contract == 2:   # 을 - 고압B - 계약III
                    if summer == 1:
                        charge_ = 8190 * self.contract_demand + self.get_precise(54.5 * used_amount[0]) + self.get_precise(106.8 * used_amount[1]) \
                                  + self.get_precise(188.1 * used_amount[2])
                    elif winter == 1:
                        charge_ = 8190 * self.contract_demand + self.get_precise(61.6 * used_amount[0]) + self.get_precise(106.8 * used_amount[1]) \
                                  + self.get_precise(163.0 * used_amount[2])
                    else:
                        charge_ = 8190 * self.contract_demand + self.get_precise(54.5 * used_amount[0]) + self.get_precise(76.9 * used_amount[1]) \
                                  + self.get_precise(107.2 * used_amount[2])
                else:
                    print("Wrong input")
            elif class2 == 2:
                if class_contract == 0:     # 을 - 고압C - 계약I
                    if summer == 1:
                        charge_ = 6590 * self.contract_demand + self.get_precise(59.5 * used_amount[0]) + self.get_precise(112.4 * used_amount[1]) \
                                  + self.get_precise(193.3 * used_amount[2])
                    elif winter == 1:
                        charge_ = 6590 * self.contract_demand + self.get_precise(66.4 * used_amount[0]) + self.get_precise(112.0 * used_amount[1]) \
                                  + self.get_precise(168.6 * used_amount[2])
                    else:
                        charge_ = 6590 * self.contract_demand + self.get_precise(59.5 * used_amount[0]) + self.get_precise(82.4 * used_amount[1]) \
                                  + self.get_precise(112.8 * used_amount[2])
                elif class_contract == 1:   # 을 - 고압C - 계약II
                    if summer == 1:
                        charge_ = 7520 * self.contract_demand + self.get_precise(54.8 * used_amount[0]) + self.get_precise(107.7 * used_amount[1]) \
                                  + self.get_precise(188.6 * used_amount[2])
                    elif winter == 1:
                        charge_ = 7520 * self.contract_demand + self.get_precise(61.7 * used_amount[0]) + self.get_precise(107.3 * used_amount[1]) \
                                  + self.get_precise(163.9 * used_amount[2])
                    else:
                        charge_ = 7520 * self.contract_demand + self.get_precise(54.8 * used_amount[0]) + self.get_precise(77.7 * used_amount[1]) \
                                  + self.get_precise(108.1 * used_amount[2])
                elif class_contract == 2:   # 을 - 고압C - 계약III
                    if summer == 1:
                        charge_ = 8090 * self.contract_demand + self.get_precise(53.7 * used_amount[0]) + self.get_precise(106.6 * used_amount[1]) \
                                  + self.get_precise(187.5 * used_amount[2])
                    elif winter == 1:
                        charge_ = 8090 * self.contract_demand + self.get_precise(60.6 * used_amount[0]) + self.get_precise(106.2 * used_amount[1]) \
                                  + self.get_precise(162.8 * used_amount[2])
                    else:
                        charge_ = 8090 * self.contract_demand + self.get_precise(53.7 * used_amount[0]) + self.get_precise(76.6 * used_amount[1]) \
                                  + self.get_precise(107.0 * used_amount[2])
                else:
                    print("Wrong input")
            else:
                print("Wrong input")
        else:
            print("Wrong input")

        return charge_      # 부가가치세, 전력산업기반기금, 필수 사용량 보장공제 제외.

