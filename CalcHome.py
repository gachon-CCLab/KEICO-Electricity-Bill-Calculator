from CalcCharge import *


class CalcHome(CalcCharge):
    def __init__(self, used_amount_list_, voltage_factor):
        self.used_amount_list = used_amount_list_
        self.voltage_factor = voltage_factor

    @staticmethod
    def get_precise(num):  # int()의 역할(즉, 내림(절삭)) + 부동소수점 오류 fix
        if (num - int(num)) != 0.5:
            if abs(round(num) - num) <= 0.01:
                num = round(num)
        return int(num)

    def init_calc(self):
        charge: int = 0
        # summer: bool = 0  # 여름
        # winter: bool = 0  # 겨울
        # voltage_factor: bool = 0  # 0: 저압, 1: 고압
        tmp_charge: float
        env_contribution, fuel_rate = CalcCharge.get_conf(self)

        for i in range(12):
            summer: bool = 0  # 여름
            winter: bool = 0  # 겨울
            if self.used_amount_list[i] != 0:
                if 6 <= i <= 7:
                    summer = 1
                elif (0 <= i <= 1) or i == 11:
                    winter = 1
                tmp_charge = self.calc(i, self.voltage_factor, summer, winter)
                result = self.get_precise(tmp_charge)  # 전기요금계(기본요금 + 전력량요금)
                if (self.used_amount_list[i] <= 200) and (result > 1000):     # 필수사용량 보장공제
                    if self.voltage_factor == 0:
                        result = result - 4000
                    if self.voltage_factor == 1:
                        result = result - 2500
                    if result < 1000:
                        result = 1000

                used_sum = self.used_amount_list[i]
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
                print("전기 요금계 :", result)
                print("부가가치세 :", tax1)
                print("전력산업기반기금 :", tax2)
                print("청구금액 :", tmp_charge, "\n")
                charge += tmp_charge

        return charge

    def calc(self, i, voltage_factor, summer, winter):
        used_amount = self.used_amount_list[i]
        charge_: float = 0
        if voltage_factor == 0:
            if winter == 1:
                if used_amount > 0 and used_amount <= 200:
                    charge_ = 910 + self.get_precise(used_amount * 93.3)
                elif used_amount > 200 and used_amount <= 400:
                    charge_ = 1600 + self.get_precise(200 * 93.3) + self.get_precise((used_amount - 200) * 187.9)
                elif used_amount > 400 and used_amount <= 1000:
                    charge_ = 7300 + 200 * 93.3 + 200 * 187.9 + self.get_precise((used_amount - 400) * 280.6)
                elif used_amount > 1000:
                    charge_ = 7300 + (200 * 93.3) + (200 * 187.9) + (600 * 280.6) + self.get_precise((
                                                                                                used_amount - 1000) * 709.5)  # 1000kWh 초과 시 슈퍼유저
                else:
                    print("Wrong input")
            elif summer == 1:
                if used_amount > 0 and used_amount <= 300:
                    charge_ = 910 + self.get_precise(used_amount * 93.3)
                elif used_amount > 300 and used_amount <= 450:
                    charge_ = 1600 + 300 * 93.3 + self.get_precise((used_amount - 300) * 187.9)
                elif used_amount > 450 and used_amount <= 1000:
                    charge_ = 7300 + 300 * 93.3 + 150 * 187.9 + self.get_precise((used_amount - 450) * 280.6)
                elif used_amount > 1000:
                    charge_ = 7300 + (300 * 93.3) + (150 * 187.9) + (550 * 280.6) + self.get_precise((
                                                                                                used_amount - 1000) * 709.5)  # 1000kWh 초과 시 슈퍼유저
                else:
                    print("Wrong input")
            else:  # 평상시
                if used_amount > 0 and used_amount <= 200:
                    charge_ = 910 + self.get_precise(used_amount * 93.3)
                elif used_amount > 200 and used_amount <= 400:
                    charge_ = 1600 + 200 * 93.3 + self.get_precise((used_amount - 200) * 187.9)
                elif used_amount > 400:  # 슈퍼 유저는 여름-겨울에만 존재
                    charge_ = 7300 + 200 * 93.3 + 200 * 187.9 + self.get_precise((used_amount - 400) * 280.6)
                else:
                    print("Wrong input")
        elif voltage_factor == 1:
            if winter == 1:
                if used_amount > 0 and used_amount <= 200:
                    charge_ = 730 + self.get_precise(used_amount * 78.3)
                elif used_amount > 200 and used_amount <= 400:
                    charge_ = 1260 + 200 * 78.3 + self.get_precise((used_amount - 200) * 147.3)
                elif used_amount > 400 and used_amount <= 1000:
                    charge_ = 6060 + 200 * 78.3 + 200 * 147.3 + self.get_precise((used_amount - 400) * 215.6)
                elif used_amount > 1000:
                    charge_ = 6060 + (200 * 78.3) + (200 * 147.3) + (600 * 215.6) + self.get_precise((
                                                                                                used_amount - 1000) * 574.6)  # 1000kWh 초과 시 슈퍼유저
                else:
                    print("Wrong input")
            elif summer == 1:
                if used_amount > 0 and used_amount <= 300:
                    charge_ = 730 + self.get_precise(used_amount * 78.3)
                elif used_amount > 300 and used_amount <= 450:
                    charge_ = 1260 + 300 * 78.3 + self.get_precise((used_amount - 300) * 147.3)
                elif used_amount > 450 and used_amount <= 1000:
                    charge_ = 6060 + 300 * 78.3 + 150 * 147.3 + self.get_precise((used_amount - 450) * 215.6)
                elif used_amount > 1000:
                    charge_ = 6060 + 300 * 78.3 + 150 * 147.3 + 550 * 215.6 + self.get_precise((
                                                                                          used_amount - 1000) * 574.6)  # 1000kWh 초과 시 슈퍼유저
                else:
                    print("Wrong input")
            else:  # 평상시
                if used_amount > 0 and used_amount <= 200:
                    charge_ = 730 + self.get_precise(used_amount * 78.3)
                elif used_amount > 200 and used_amount <= 400:
                    charge_ = 1260 + 200 * 78.3 + self.get_precise((used_amount - 200) * 147.3)
                elif used_amount > 400:  # 슈퍼 유저는 여름-겨울에만 존재
                    charge_ = 6060 + 200 * 78.3 + 200 * 147.3 + self.get_precise((used_amount - 400) * 215.6)
                else:
                    print("Wrong input")
        else:
            print("Wrong input")

        return charge_  # 부가가치세, 전력산업기반기금, 필수 사용량 보장공제 제외.
