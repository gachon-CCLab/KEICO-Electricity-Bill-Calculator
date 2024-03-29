# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import datetime

from typing import List

from MonthCalc import *

# POST (JSON)
headers = {'Content-Type': 'application/json; charset=utf-8'}

month_calc = MonthCalc()
user_data = month_calc.user_data
result_index = 1
calc_type = month_calc.user_data.calc_type

dt_parser = lambda x: datetime.strptime(x[:-6], "%Y-%m-%d %H:%M:%S")


def get_data_list() -> list:
    used_amount_list: List[List[float]] = [[0.0 for i in range(3)] for j in range(12)]
    data_df = pd.read_csv('future_5min_total.csv',
                          index_col=['date'],
                          parse_dates=['date'],
                          date_parser=dt_parser,
                          infer_datetime_format=True,
                          delimiter=',')
    months_df = [g for n, g in data_df.groupby(pd.Grouper(freq='M'))]
    print(months_df)

    print(len(months_df))
    print(months_df[0])

    # calc_type = 0

    for month_df in months_df:
        print(type(month_df))
        target_month = month_df.index.month[0]
        if calc_type == 0:  # 주택용
            # 단순 합산 후 데이터 input
            sum_df = month_df['total1'].resample('1M').sum()
            used_amount_list[target_month + 1][0] = sum_df[0]
        else:  # 일반용, 산업용
            off_peak_df = month_df[(month_df.index.hour < 9) | (month_df.index.hour >= 23)]
            # 계시별 요금제 처리
            if 2 <= target_month < 11:
                mid_peak_df = month_df[
                    ((month_df.index.hour >= 9) & (month_df.index.hour < 10)) |
                    ((month_df.index.hour >= 12) & (month_df.index.hour < 13)) |
                    ((month_df.index.hour >= 17) & (month_df.index.hour < 23))]
                on_peak_df = month_df[
                    ((month_df.index.hour >= 10) & (month_df.index.hour < 12)) |
                    ((month_df.index.hour >= 13) & (month_df.index.hour < 17))]
            else:
                mid_peak_df = month_df[
                    ((month_df.index.hour >= 9) & (month_df.index.hour < 10)) |
                    ((month_df.index.hour >= 12) & (month_df.index.hour < 13)) |
                    ((month_df.index.hour >= 17) & (month_df.index.hour < 23))]
                on_peak_df = month_df[
                    ((month_df.index.hour >= 10) & (month_df.index.hour < 12)) |
                    ((month_df.index.hour >= 13) & (month_df.index.hour < 17))]
            off_sum_df = off_peak_df['total1'].resample('1M').sum() / 1000.0
            mid_sum_df = mid_peak_df['total1'].resample('1M').sum() / 1000.0
            on_sum_df = on_peak_df['total1'].resample('1M').sum() / 1000.0

            # 월간 합을 사용량 리스트에 저장
            try:    # 일부 데이터만 있는 경우 대응
                used_amount_list[target_month - 1] = [off_sum_df[0], mid_sum_df[0], on_sum_df[0]]
            except IndexError as ie:
                print(ie)
                pass
    return used_amount_list


month_calc.user_data.used_amount_list = get_data_list()

# 비교 세트, 일반용과 산업용에 적용 가능
# a number = class1 * 100 + class2 * 10 + class3 * 1
comparison_set1 = (10, 11, 100, 101)
comparison_set2 = (20, 21, 110, 111)
comparison_set3 = (200, 201, 202)
comparison_set4 = (210, 211, 212)
comparison_set5 = (220, 221, 222)
comparison_sets = [comparison_set1, comparison_set2, comparison_set3,
                   comparison_set4, comparison_set5]

selector = user_data.class1 * 100 + user_data.class2 * 10 + user_data.class_contract

target_set_idx = None
target_sets: list
result_list = [0.0 for i in range(12)]

# input data의 selector가 비교 set에 해당할 경우 해당 index를 저장
for i in range(5):
    for a_selector in comparison_sets[i]:
        if selector == a_selector:
            target_set_idx = i

# json file import.
with open("electric_rates.json", "r", encoding="utf-8") as f_rates_json:
    rates_data = json.load(f_rates_json)
    f_rates_json.close()

# 현재 요금제 기반 요금계산
for i in range(1, 13):
    result_list[i - 1] = month_calc.get_result(user_data, i)

# 요금 데이터로부터 계산할 요금의 세부정보 얻기
target_gen_obj = (item for item in rates_data['electric_rates'] if item['calc_type'] == calc_type and item['class1']
                  == user_data.class1 and item['class2'] == user_data.class2 and item[
                      'class_contract'] == user_data.class_contract)
for value in target_gen_obj:
    target_rates_dict = value
rates_title = target_rates_dict['description']

data = {'title': 'result', 'id': 0, 'selector': selector,
        'rates_title': rates_title, 'result_list': result_list,
        'used_amount_list': month_calc.user_data.used_amount_list}
res = requests.post('http://127.0.0.1:3000',
                    data=json.dumps(data), headers=headers)

if target_set_idx is not None:  # 비교군이 존재하는 요금일 경우.

    # 현재 사용하는 요금을 비교군에서 제거
    target_sets = list(comparison_sets[target_set_idx])
    target_sets.remove(selector)

    for comparable_selector in target_sets:
        user_data.class1 = comparable_selector // 100
        user_data.class2 = (comparable_selector % 100) // 10
        user_data.class_contract = (comparable_selector % 10)

        # 요금 데이터로부터 계산할 요금의 세부정보 얻기
        target_gen_obj = (item for item in rates_data['electric_rates'] if
                          item['calc_type'] == calc_type and item['class1']
                          == user_data.class1 and item['class2'] == user_data.class2 and item[
                              'class_contract'] == user_data.class_contract)
        for value in target_gen_obj:
            target_rates_dict = value
        rates_title = target_rates_dict['description']

        # 1년(12개월)에 해당하는 계산 
        for i in range(1, 13):
            result_list[i - 1] = month_calc.get_result(user_data, i)

        data = {'title': 'result', 'id': result_index, 'selector': comparable_selector, 'rates_title': rates_title,
                'result_list': result_list}
        res = requests.post('http://127.0.0.1:3000', data=json.dumps(data), headers=headers)

        result_index += 1
else:
    print("not included")
    # result = month_calc.get_result(user_data)
    # data = {'title': 'result', 'id': result_index,
    #         'selector': comparable_selector, 'result_list': result_list}
    # res = requests.post('http://127.0.0.1:3000',
    #                     data=json.dumps(data), headers=headers)

# 리스트에 있는대로 서버에 API 전달

# 현재 사용중인 요금제는 리스트에서 제거


# POST (JSON)
# data = {'title': 'finish'}
# res = requests.post('http://127.0.0.1:3000', data=json.dumps(data), headers=headers)
print(str(res.status_code) + " | " + res.text)
