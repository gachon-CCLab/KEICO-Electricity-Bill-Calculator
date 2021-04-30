from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import time
from selenium import webdriver


class Parser:
    def __init__(self, selector, used_amount_list_, contract_demand, class1, class2, class_contract):
        # 0: 주택용(저압), 1: 주택용(고압), 2: 일반용(갑)I, 3: 일반용(갑)II
        # 4: 일반용(을),  5: 산업용(갑)I,  6: 산업용(갑)II, 7: 산업용(을)
        self.selector = selector
        self.used_amount_list = used_amount_list_
        self.contract_demand = contract_demand
        self.class1 = class1
        self.class2 = class2
        self.class_contract = class_contract

    def init_calc(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome('chromedriver', chrome_options=options)
        driver.get("http://cyber.kepco.co.kr/ckepco/front/jsp/CY/J/A/CYJAPP000NFL.jsp#")
        wait = WebDriverWait(driver, 10)

        element = wait.until(EC.element_to_be_clickable((By.ID, 'bill_simulation')))
        element.click()

        charge: int = 0
        result_: str = ''

        if self.selector == 0:  # 주택용(저압)
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '주택용(저압)')))
            element.click()
            for i in range(12):
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-trigger')))
                if self.used_amount_list[i] != 0:
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i+1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'HouseL_input_04')))
                    elem.clear()
                    elem.send_keys(self.used_amount_list[i])
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 1:    # 주택용(고압)
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '주택용(고압)')))
            element.click()
            for i in range(12):
                element = wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, '#FormHouseH > tbody > tr:nth-child(5) > td > div > img')))
                if self.used_amount_list[i] != 0:
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'HouseH_input_04')))
                    elem.clear()
                    elem.send_keys(self.used_amount_list[i])
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 2:    # 일반용(갑)Ⅰ
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '일반용(갑)Ⅰ')))
            element.click()
            for i in range(12):
                if self.used_amount_list[i] != 0:
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK_input_01')))
                    element.clear()
                    element.send_keys(str(self.contract_demand))
                    element = Select(wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK_input_05'))))
                    if self.class2 == 0 and self.class_contract == 0:
                        element.select_by_index(1)  # 저압전력
                    elif self.class2 == 1 and self.class_contract == 0:
                        element.select_by_index(2)  # 고압A:선택 I
                    elif self.class2 == 1 and self.class_contract == 1:
                        element.select_by_index(3)  # 고압A:선택 II
                    elif self.class2 == 2 and self.class_contract == 0:
                        element.select_by_index(4)  # 고압B:선택 I
                    elif self.class2 == 2 and self.class_contract == 1:
                        element.select_by_index(5)  # 고압B:선택 II
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK_input_06')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][0])
                    # element = wait.until(EC.element_to_be_clickable((
                    #     By.CSS_SELECTOR, '#FormHouseH > tbody > tr:nth-child(5) > td > div > img')))
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#FormGeneralK > tbody > tr:nth-child(9) > td > div > img')))
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 3:    # 일반용(갑)Ⅱ
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '일반용(갑)Ⅱ')))
            element.click()
            for i in range(12):
                if self.used_amount_list[i] != 0:
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK2_input_01')))
                    element.clear()
                    element.send_keys(str(self.contract_demand))
                    element = Select(wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK2_input_05'))))
                    if self.class2 == 0 and self.class_contract == 0:
                        element.select_by_index(1)  # 고압A:선택 I
                    elif self.class2 == 0 and self.class_contract == 1:
                        element.select_by_index(2)  # 고압A:선택 II
                    elif self.class2 == 1 and self.class_contract == 0:
                        element.select_by_index(3)  # 고압B:선택 I
                    elif self.class2 == 1 and self.class_contract == 1:
                        element.select_by_index(4)  # 고압B:선택 II
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK2_input_07')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][1])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK2_input_08')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][2])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralK2_input_09')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][0])
                    element = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#FormGeneralK2 > tbody > tr:nth-child(12) > td > div > img')))
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 4:    # 일반용(을)
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '일반용(을)')))
            element.click()
            for i in range(12):
                if self.used_amount_list[i] != 0:
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralU_input_01')))
                    element.clear()
                    element.send_keys(str(self.contract_demand))
                    element = Select(wait.until(EC.element_to_be_clickable((By.ID, 'GeneralU_input_05'))))
                    if self.class2 == 0 and self.class_contract == 0:
                        element.select_by_index(1)  # 고압A:선택 I
                    elif self.class2 == 0 and self.class_contract == 1:
                        element.select_by_index(2)  # 고압A:선택 II
                    elif self.class2 == 0 and self.class_contract == 2:
                        element.select_by_index(3)  # 고압A:선택 III
                    elif self.class2 == 1 and self.class_contract == 0:
                        element.select_by_index(4)  # 고압B:선택 I
                    elif self.class2 == 1 and self.class_contract == 1:
                        element.select_by_index(5)  # 고압B:선택 II
                    elif self.class2 == 1 and self.class_contract == 2:
                        element.select_by_index(6)  # 고압B:선택 III
                    elif self.class2 == 2 and self.class_contract == 0:
                        element.select_by_index(7)  # 고압C:선택 I
                    elif self.class2 == 2 and self.class_contract == 1:
                        element.select_by_index(8)  # 고압C:선택 II
                    elif self.class2 == 2 and self.class_contract == 2:
                        element.select_by_index(9)  # 고압C:선택 III
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralU_input_07')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][1])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralU_input_08')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][2])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'GeneralU_input_09')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][0])
                    element = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#FormGeneralU > tbody > tr:nth-child(12) > td > div > img')))
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 5:  # 산업용(갑) I
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '산업용(갑)Ⅰ')))
            element.click()
            for i in range(12):
                if self.used_amount_list[i] != 0:
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK_input_01')))
                    element.clear()
                    element.send_keys(str(self.contract_demand))
                    element = Select(wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK_input_05'))))
                    if self.class2 == 0 and self.class_contract == 0:
                        element.select_by_index(1)   # 저압전력
                    elif self.class2 == 1 and self.class_contract == 0:
                        element.select_by_index(2)   # 고압A:선택 I
                    elif self.class2 == 1 and self.class_contract == 1:
                        element.select_by_index(3)   # 고압A:선택 II
                    elif self.class2 == 2 and self.class_contract == 0:
                        element.select_by_index(4)   # 고압B:선택 I
                    elif self.class2 == 2 and self.class_contract == 1:
                        element.select_by_index(5)   # 고압B:선택 II
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK_input_06')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][0])
                    element = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#FormIndustryK > tbody > tr:nth-child(8) > td > div > img')))
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 6:  # 산업용(갑) II
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '산업용(갑)Ⅱ')))
            element.click()
            for i in range(12):
                if self.used_amount_list[i] != 0:
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK2_input_01')))
                    element.clear()
                    element.send_keys(str(self.contract_demand))
                    element = Select(wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK2_input_05'))))
                    if self.class2 == 0 and self.class_contract == 0:
                        element.select_by_index(1)  # 고압A:선택 I
                    elif self.class2 == 0 and self.class_contract == 1:
                        element.select_by_index(2)  # 고압A:선택 II
                    elif self.class2 == 1 and self.class_contract == 0:
                        element.select_by_index(3)  # 고압B:선택 I
                    elif self.class2 == 1 and self.class_contract == 1:
                        element.select_by_index(4)  # 고압B:선택 II
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK2_input_07')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][1])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK2_input_08')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][2])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryK2_input_09')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][0])
                    element = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#FormIndustryK2 > tbody > tr:nth-child(11) > td > div > img')))
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.presence_of_element_located((By.ID, 'cal_result')))
                            # elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        elif self.selector == 7:  # 산업용(을)
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '산업용(을)')))
            element.click()
            for i in range(12):
                if self.used_amount_list[i] != 0:
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryU_input_01')))
                    element.clear()
                    element.send_keys(str(self.contract_demand))
                    element = Select(wait.until(EC.element_to_be_clickable((By.ID, 'IndustryU_input_05'))))
                    if self.class2 == 0 and self.class_contract == 0:
                        element.select_by_index(1)  # 고압A:선택 I
                    elif self.class2 == 0 and self.class_contract == 1:
                        element.select_by_index(2)  # 고압A:선택 II
                    elif self.class2 == 0 and self.class_contract == 2:
                        element.select_by_index(3)  # 고압A:선택 III
                    elif self.class2 == 1 and self.class_contract == 0:
                        element.select_by_index(4)  # 고압B:선택 I
                    elif self.class2 == 1 and self.class_contract == 1:
                        element.select_by_index(5)  # 고압B:선택 II
                    elif self.class2 == 1 and self.class_contract == 2:
                        element.select_by_index(6)  # 고압B:선택 III
                    elif self.class2 == 2 and self.class_contract == 0:
                        element.select_by_index(7)  # 고압C:선택 I
                    elif self.class2 == 2 and self.class_contract == 1:
                        element.select_by_index(8)  # 고압C:선택 II
                    elif self.class2 == 2 and self.class_contract == 2:
                        element.select_by_index(9)  # 고압C:선택 III
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryU_input_07')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][1])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryU_input_08')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][2])
                    element = wait.until(EC.element_to_be_clickable((By.ID, 'IndustryU_input_09')))
                    element.clear()
                    element.send_keys(self.used_amount_list[i][0])
                    element = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#FormIndustryU > tbody > tr:nth-child(11) > td > div > img')))
                    element.click()
                    time.sleep(0.5)
                    element2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month')))
                    element2.click()
                    element2.send_keys(str(i + 1) + '월')
                    element2.click()
                    time.sleep(0.5)
                    element3 = driver.find_elements_by_class_name("ui-state-default")
                    k = 0
                    while 1:
                        if element3[k].text == '1':
                            break
                        k += 1
                    element3[k].click()
                    elem = wait.until(EC.element_to_be_clickable((By.ID, 'cal_start')))
                    elem.click()
                    time.sleep(0.1)
                    while True:
                        try:
                            elem = wait.until(EC.visibility_of_element_located((By.ID, 'cal_result')))
                            result_ = elem.text
                            result_ = result_.replace('\n', '').replace('계산된 금액은', '').replace('원 입니다.', '').replace(
                                ',', '')
                            if "    " in result_:   # 텍스트 잘 못 찾을 때의 예외처리
                                continue
                            print('result : ' + result_)
                            charge += int(result_)
                            break
                        except ValueError as v:
                            print(v)
            driver.quit()
            return int(charge)

        # else:
        #     print("Wrong input")


# #####TEST-HOME###############################################################
# used_amount_list_home: list[int] = [0 for i in range(12)]
# used_amount_list_home[0] = 1204      # 1월 사용량
# used_amount_list_home[1] = 1203
# used_amount_list_home[2] = 1202
# used_amount_list_home[3] = 1201
# used_amount_list_home[4] = 1111
# used_amount_list_home[5] = 1123
# used_amount_list_home[6] = 1213
# used_amount_list_home[7] = 1521
# used_amount_list_home[8] = 1234
# used_amount_list_home[9] = 1123
# used_amount_list_home[10] = 1423
# used_amount_list_home[11] = 1204
# print(used_amount_list_home)
# #############################################################################
#
# #####TEST-General###############################################################
# used_amount_list_general = [[0 for i in range(3)] for j in range(12)]
# used_amount_list_general[0] = [1, 1, 1]      # 1월 사용량   # 계약전력으로 구분되지 않을 경우 index [0]에 사용량.
# used_amount_list_general[1] = [1, 1, 1]
# used_amount_list_general[2] = [1, 1, 1]
# used_amount_list_general[3] = [1, 1, 1]
# used_amount_list_general[4] = [1, 1, 1]
# used_amount_list_general[5] = [1, 1, 1]
# used_amount_list_general[6] = [1, 1, 1]
# used_amount_list_general[7] = [5, 300, 20]
# used_amount_list_general[8] = [1, 1, 1]
# used_amount_list_general[9] = [1, 1, 1]
# used_amount_list_general[10] = [1, 1, 1]
# used_amount_list_general[11] = [1, 1, 1]
# contract_demand = 10
# class1 = 0
# class2 = 1
# class_contract = 0
# print(used_amount_list_general)
# #############################################################################
#
# #####TEST-Industry###############################################################
# used_amount_list_industry = [[0 for i in range(3)] for j in range(12)]
# used_amount_list_industry[0] = [1, 1, 1]  # 1월 사용량   # 계약전력으로 구분되지 않을 경우 index [0]에 사용량.
# used_amount_list_industry[1] = [1, 1, 1]
# used_amount_list_industry[2] = [1, 1, 1]
# used_amount_list_industry[3] = [1, 1, 1]
# used_amount_list_industry[4] = [1, 1, 1]
# used_amount_list_industry[5] = [1, 1, 1]
# used_amount_list_industry[6] = [1, 1, 1]
# used_amount_list_industry[7] = [5, 300, 20]
# used_amount_list_industry[8] = [1, 1, 1]
# used_amount_list_industry[9] = [1, 1, 1]
# used_amount_list_industry[10] = [1, 1, 1]
# used_amount_list_industry[11] = [1, 1, 1]
# # contract_demand = 10
# # class1 = 0
# # class2 = 0
# # class_contract = 0
# # print(used_amount_list_industry)
# #############################################################################
#
# # a = Parser(1, used_amount_list_home, 0, 0, 0, 0)
# # result: int = a.init_calc()
# # print(result)
#
# # KEPCO_Parser = Parser(7, used_amount_list_general, contract_demand, class1, class2, class_contract)
# # KEPCO_result: int = KEPCO_Parser.init_calc()
# # print(KEPCO_result)
#
#
#
