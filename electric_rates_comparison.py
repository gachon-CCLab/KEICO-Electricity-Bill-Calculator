import requests
import json
from MonthCalc import *

# POST (JSON)
headers = {'Content-Type': 'application/json; charset=utf-8'}

month_calc = MonthCalc
user_data = month_calc.user_data

# 비교 세트, 일반용과 산업용에 적용 가능
# a number = class1 * 100 + class2 * 10 + class3 * 1
comparison_set1 = (10, 11, 100, 101)
comparison_set2 = (20, 21, 110, 111)
comparison_set3 = (200, 201, 202)
comparison_set4 = (210, 211, 212)
comparison_set5 = (220, 221, 222)
comparison_sets = (comparison_set1, comparison_set2, comparison_set3,
                comparison_set4, comparison_set5)

selector = month_calc.class1 * 100 + month_calc.class2 * 10 + month_calc.class_contract 

target_set_idx = None

# input data의 selector가 비교 set에 해당할 경우 해당 index를 저장
for i in range(1, 6):
    for num in comparison_sets[i]:
        if selector == num:
            target_set_idx = i

# json file import.
with open ("electric_rates.json", "r", encoding="utf-8") as f_rates_json:
    rates_data = json.load(f_rates_json)
    f_rates_json.close()

# 현재 요금제 기반 요금계산
data = {'title': 'result', 'id': 0,}

if target_set_idx != None:      # 비교군이 존재하는 요금일 경우.

    # 현재 사용하는 요금을 비교군에서 제거
    target_sets = comparison_sets[target_set_idx].remove(selector)

    for comparable_selector in target_sets:
        user_data.class1 = comparable_selector // 100
        user_data.class2 = (comparable_selector % 100) // 10
        user_data.class_contract = (comparable_selector % 10)

        result = month_calc.getResult(month_calc.user_data)

        data = {'title': 'result', 'id': 0,}
else:
    result = month_calc.getResult(month_calc.user_data)


# 리스트에 있는대로 서버에 API 전달 

# 현재 사용중인 요금제는 리스트에서 제거


# POST (JSON)
data = {'title': 'result', 'id': 0, 'message': ''}
res = requests.post('http://127.0.0.1:5000', data=json.dumps(data), headers=headers)
print(str(res.status_code + " | " + res.text))

