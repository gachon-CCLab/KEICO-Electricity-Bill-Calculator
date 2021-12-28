from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class UserData:
    # used_amount_list: list[int] = field(default_factory=list)
    used_amount_list: list[int]# 계약 전력(kWh)  # 4kWh 이상?
    contract_demand: int
    charge: float
    voltage_factor: int     # 0: 저압, 1: 고압 (in home Calc)

    calc_type: int      # 0: 주택용, 1: 일반용, 2: 산업용

    # 0: 갑I, 1: 갑II, 2: 을
    class1: int

    # 갑I  -> 0: 저압,  1: 고압A, 2: 고압B
    # 갑II -> 0: 고압A, 1: 고압B
    # 을   -> 0: 고압A, 1: 고압B, 2: 고압C
    class2: int

    class_contract: int

    # def __post_init__(self):
    #     self.used_amount_list = [0 for i in range(12)]
    #     self.contract_demand = 0
    #     self.charge = 0
    #     self.voltage_factor = 0
    #     self.class1 = 0
    #     self.class2 = 0
    #     self.class_contract = 0


