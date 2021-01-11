import pymysql
from calc_Charge.CalcHome import *
from calc_Charge.CalcGeneral import *
from calc_Charge.CalcIndustry import *
import pandas as pd
import datetime


def seperateResult(_result):
    result = _result
    date_time = result[0]['DATE']
    print(date_time.hour)

    users_uid = result[0]['USERS_UID']
    pid = result[0]['PID']
    contract_kw = result[0]['CONTRACT_KW']
    usage = result[0]['USAGE']  # 전기 사용량
    tmp = result[0]['SELECTOR']
    year = date_time.year
    month = date_time.month
    hour = date_time.hour
    selector = tmp // 100  # 100의 자리
    class2 = (tmp % 100) // 10  # 10의 자리
    class_contract = tmp % 10  # 1의 자리

    light_load_kw = 0
    mid_load_kw = 0
    peak_load_kw = 0

    if 0 <= selector <= 1:
        if 6 <= month <= 7:
            summer = 1
        elif (0 <= month <= 1) or month == 11:
            winter = 1
        light_load_kw = usage
    elif 2 <= selector <= 7:
        if 5 <= month <= 7:
            summer = 1
            if (0 <= hour < 9) or (23 <= hour < 24):
                light_load_kw = usage
            elif (9 <= hour < 10) or (12 <= hour < 13):
                mid_load_kw = usage
            elif (10 <= hour < 12) or (13 <= hour < 17):
                peak_load_kw = usage
            else:
                print("Wrong input")
        elif (0 <= month <= 1) or (10 <= month <= 11):
            winter = 1
            if (0 <= hour < 12) or (23 <= hour < 24):
                light_load_kw = usage
            elif (12 <= hour < 17) or (20 <= hour < 22):
                mid_load_kw = usage
            elif (17 <= hour < 20) or (22 <= hour < 23):
                peak_load_kw = usage
            else:
                print("Wrong input")
        else:
            print("Wrong input")

        if (0 <= hour < 9) or (23 <= hour < 24):
            light_load_kw = usage
        elif (9 <= hour < 10) or (12 <= hour < 13):
            mid_load_kw = usage
        elif (10 <= hour < 12) or (13 <= hour < 17):
            peak_load_kw = usage
        else:
            print("Wrong input")
    else:
        print("Wrong input")

    data = (year, month, users_uid, pid, contract_kw, light_load_kw, mid_load_kw, peak_load_kw, tmp)

    return data


def convertToMonth(db):
    mysql_local = db

    # DB - cursor()
    cursor = mysql_local.cursor(pymysql.cursors.DictCursor)

    # Test #
    sql = "SELECT * FROM USER_DATA;"  # 조건 바꿔서 원하는 튜플만 수집
    cursor.execute(sql)
    result = cursor.fetchall()  # 딕셔너리가 모인 리스트로 반환
    print(result)
    print(result[1]['DATE'])

    data = seperateResult(result)

    sql = "INSERT INTO MONTH_DATA (YEAR, MONTH, USERS_UID, PID, CONTRACT_KW, LIGHT_LOAD_KW, MID_LOAD_KW, " \
          "PEAK_LOAD_KW, SELECTOR) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s); "
    cursor.execute(sql, data)
    mysql_local.commit()

    sql = "SELECT * FROM MONTH_DATA;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    ########################################################


# 요금 계산 처리 후 DB에 넣을 수 있도록 정렬된 값 return
def calcResult(_result):
    result = _result

    year = result[0]['YEAR']
    month = result[0]['MONTH']
    users_uid = result[0]['USERS_UID']
    pid = result[0]['PID']
    contract_kw = result[0]['CONTRACT_KW']
    light_load_kw = result[0]['LIGHT_LOAD_KW']
    mid_load_kw = result[0]['MID_LOAD_KW']
    peak_load_kw = result[0]['PEAK_LOAD_KW']
    tmp = result[0]['SELECTOR']
    selector = tmp // 100  # 100의 자리
    class2 = (tmp % 100) // 10  # 10의 자리
    class_contract = tmp % 10  # 1의 자리
    light_load_krw = 0
    mid_load_krw = 0
    peak_load_krw = 0
    class1 = 0

    if 0 <= selector <= 1:
        a = CalcHome(light_load_kw, selector)
        light_load_krw = int(a.init_calc())
    elif 1 < selector <= 4:
        if selector == 2:
            class1 = 0
        elif selector == 3:
            class1 = 1
        elif selector == 4:
            class1 = 2
        else:
            print("Error")
        for k in range(3):
            used_amount_list_general = [[0 for i in range(3)] for j in range(12)]  # 2차원 배열 초기화
            if k == 0:
                used_amount_list_general[month-1][0] = light_load_kw
                b = CalcGeneral(used_amount_list_general, contract_kw, class1, class2, class_contract)
                light_load_krw = b.init_calc()
            elif k == 1:
                used_amount_list_general[month - 1][0] = mid_load_kw
                b = CalcGeneral(used_amount_list_general, contract_kw, class1, class2, class_contract)
                mid_load_krw = b.init_calc()
            elif k == 2:
                used_amount_list_general[month - 1][0] = peak_load_kw
                b = CalcGeneral(used_amount_list_general, contract_kw, class1, class2, class_contract)
                peak_load_krw = b.init_calc()
            else:
                print("Error")
    elif 4 < selector <= 7:
        if selector == 5:
            class1 = 0
        elif selector == 6:
            class1 = 1
        elif selector == 7:
            class1 = 2
        else:
            print("Error")
        for k in range(3):
            used_amount_list_industry = [[0 for i in range(3)] for j in range(12)]  # 2차원 배열 초기화
            if k == 0:
                used_amount_list_industry[month - 1][0] = light_load_kw
                c = CalcIndustry(used_amount_list_industry, contract_kw, class1, class2, class_contract)
                light_load_krw = c.init_calc()
            elif k == 1:
                used_amount_list_industry[month - 1][0] = mid_load_kw
                c = CalcIndustry(used_amount_list_industry, contract_kw, class1, class2, class_contract)
                mid_load_krw = c.init_calc()
            elif k == 2:
                used_amount_list_industry[month - 1][0] = peak_load_kw
                c = CalcIndustry(used_amount_list_industry, contract_kw, class1, class2, class_contract)
                peak_load_krw = c.init_calc()
    else:
        print("Error")

    data = (year, month, users_uid, pid, light_load_krw, mid_load_krw, peak_load_krw, tmp)

    print(data)
    return data


def convertToCost(db):
    mysql_local = db

    # DB - cursor()
    cursor = mysql_local.cursor(pymysql.cursors.DictCursor)

    # Test #
    sql = "SELECT * FROM MONTH_DATA;"  # 조건 바꿔서 원하는 튜플만 수집
    cursor.execute(sql)
    result = cursor.fetchall()        # 딕셔너리가 모인 리스트로 반환
    print(result)
    print(result[0])

    data = calcResult(result)

    sql = "INSERT INTO MONTH_COST (YEAR, MONTH, USERS_UID, PID, LIGHT_LOAD_KRW, MID_LOAD_KRW, PEAK_LOAD_KRW, SELECTOR)" \
          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, data)
    mysql_local.commit()

    sql = "SELECT * FROM MONTH_COST;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    ########################################################


if __name__ == '__main__':
    # DB - connect()
    _mysql_local = pymysql.connect(
        user='root',
        passwd='giai2017',
        host='127.0.0.1',
        db='testdb',
        port=3306,
        charset='utf8'
    )
    convertToMonth(_mysql_local)
    convertToCost(_mysql_local)





