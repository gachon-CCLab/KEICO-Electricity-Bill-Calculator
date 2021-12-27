import requests
import json
from MonthCalc import *

# POST (JSON)
headers = {'Content-Type': 'application/json; charset=utf-8'}

month_calc = MonthCalc
user_data = month_calc.user_data
month_calc.getResult(month_calc.user_data)

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

for i in range(1, 6):
    for num in comparison_sets[i]:
        if selector == num:
            target_set_idx = i

for comparable_selector in comparison_sets[target_set_idx]:
    user_data.class1 = comparable_selector // 100
    user_data.class2 = (comparable_selector % 100) // 10
    user_data.class_contract = (comparable_selector % 10)



# POST (JSON)
data = {'title': 'result', 'id': 0, 'message': ''}
res = requests.post('http://127.0.0.1:5000', data=json.dumps(data), headers=headers)
print(str(res.status_code + " | " + res.text))