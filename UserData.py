from dataclasses import dataclass

@dataclass
class User:
    used_amount_list_home: list[int] = [0 for i in range]
