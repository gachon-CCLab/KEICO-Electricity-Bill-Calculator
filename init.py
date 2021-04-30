import pymysql
from CalcHome import *
from CalcGeneral import *
from CalcIndustry import *
import pandas as pd
import datetime


# UPDATE
# convertToMonth의 계산부
def seperateResult(_result):
    result = _result

    # sql = "SELECT COUNT(*) FROM USER_DATA WHERE UID = %s;"
    # result = cursor.execute(sql)
    # len(result)     # 한 달 동안 한 유저의 사용 내역의 길이

    # DB로부터 받아온 데이터를 분해 및 변수에 저장
    date_time = result[0]['DATE']
    # print(date_time.hour)
    users_uid = result[0]['USERS_UID']
    pid = result[0]['PID']
    contract_kw = result[0]['CONTRACT_KW']
    usage = 0   # 전기 사용량
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

    for i in range(len(result)):
        usage = result[i]['USAGE']  # 전기 사용량

        # 전기 계약별로 다른 기능 취함
        if 0 <= selector <= 1:
            if 6 <= month <= 7:
                summer = 1
            elif (0 <= month <= 1) or month == 11:
                winter = 1
            light_load_kw += usage
        elif 2 <= selector <= 7:
            if 5 <= month <= 7:
                summer = 1
                if (0 <= hour < 9) or (23 <= hour < 24):
                    light_load_kw += usage
                elif (9 <= hour < 10) or (12 <= hour < 13):
                    mid_load_kw += usage
                elif (10 <= hour < 12) or (13 <= hour < 17):
                    peak_load_kw += usage
                else:
                    print("Wrong input")
            elif (0 <= month <= 1) or (10 <= month <= 11):
                winter = 1
                if (0 <= hour < 12) or (23 <= hour < 24):
                    light_load_kw += usage
                elif (12 <= hour < 17) or (20 <= hour < 22):
                    mid_load_kw += usage
                elif (17 <= hour < 20) or (22 <= hour < 23):
                    peak_load_kw += usage
                else:
                    print("Wrong input")
            else:
                print("Wrong input")

            if (0 <= hour < 9) or (23 <= hour < 24):
                light_load_kw += usage
            elif (9 <= hour < 10) or (12 <= hour < 13):
                mid_load_kw += usage
            elif (10 <= hour < 12) or (13 <= hour < 17):
                peak_load_kw += usage
            else:
                print("Wrong input")
        else:
            print("Wrong input")

    data = (year, month, users_uid, contract_kw, light_load_kw, mid_load_kw, peak_load_kw, tmp)

    return data


# UPDATE
# user_data to month_data
def convertToMonth(db, info):
    mysql_local = db
    uid_pid = info

    # DB - cursor()
    cursor = mysql_local.cursor(pymysql.cursors.DictCursor)

    # Test #
    sql = "SELECT * FROM USER_DATA;"  # 조건 바꿔서 원하는 튜플만 수집
    cursor.execute(sql)
    # sql = "SELECT * FROM USER_DATA WHERE UID = %s AND PID = %s;"
    # result = cursor.execute(sql, uid_pid)
    result = cursor.fetchall()  # 딕셔너리가 모인 리스트로 반환
    print(result)
    # print(result[0]['DATE'])

    data = seperateResult(result)

    sql = "INSERT INTO MONTH_DATA (YEAR, MONTH, USERS_UID, CONTRACT_KW, LIGHT_LOAD_KW, MID_LOAD_KW, " \
          "PEAK_LOAD_KW, SELECTOR) VALUES(%s, %s, %s, %s, %s, %s, %s, %s); "
    cursor.execute(sql, data)
    mysql_local.commit()

    sql = "SELECT * FROM MONTH_DATA;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    ########################################################


# UPDATE
# convertToCost의 계산부
# 요금 계산 처리 후 DB에 넣을 수 있도록 정렬된 값 return
def calcResult(_result):
    result = _result

    # DB로부터 받아온 데이터를 분해 및 변수에 저장
    year = result[0]['YEAR']
    month = result[0]['MONTH']
    users_uid = result[0]['USERS_UID']
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

    used_amount_list_home = [0 for i in range(12)]
    used_amount_list_home[month-1] = light_load_kw

    # 전기 계약별로 다른 기능 취함
    if 0 <= selector <= 1:
        a = CalcHome(used_amount_list_home, selector)
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
                used_amount_list_general[month - 1][1] = mid_load_kw
                b = CalcGeneral(used_amount_list_general, contract_kw, class1, class2, class_contract)
                mid_load_krw = b.init_calc()
            elif k == 2:
                used_amount_list_general[month - 1][2] = peak_load_kw
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

    data = (year, month, users_uid, light_load_krw, mid_load_krw, peak_load_krw, tmp)

    print(data)
    return data


# UPDATE
# month_data to month_cost
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

    # 다음 테이블에 들어갈 data 생성
    data = calcResult(result)

    # SQL
    sql = "INSERT INTO MONTH_COST (YEAR, MONTH, USERS_UID, LIGHT_LOAD_KRW, MID_LOAD_KRW, PEAK_LOAD_KRW, SELECTOR)" \
          "VALUES(%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, data)
    mysql_local.commit()

    sql = "SELECT * FROM MONTH_COST;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    ########################################################


# Working
# CREATE
# 딕셔너리를 받아 user_data에 새로운 유저 데이터를 insert 해줌.
def insertUserData(db, _dict):   # dict : DATE / USERS_UID / PID / CONTRACT_KW / USAGE / SELECTOR
    mysql_local = db

    # DB - cursor()
    cursor = mysql_local.cursor(pymysql.cursors.DictCursor)

    sql = "INSERT INTO user_data VALUES(%s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, _dict)
    db.commit()


# Working
# READ
# 유저의 전기 사용량 조회
def showUsage(db, user_info):   # user_info : dictionary
    mysql_local = db

    # DB - cursor()
    cursor = mysql_local.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT USAGE FROM month_data WHERE UID = %s AND PID = %s; "


# Working
# DELETE
# 유저의 데이터 일괄 삭제



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

    # ### TEST ######
    info = (1, 1)   # info = (month, uid)

    ################

    # 요금 계산이 필요할 경우에 실행
    convertToMonth(_mysql_local, info)
    convertToCost(_mysql_local)





