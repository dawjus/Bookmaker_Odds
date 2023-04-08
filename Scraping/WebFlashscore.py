from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import pandas as pd
import time
import math

def flashscore(path='https://www.flashscore.com', deltaDate =0):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument("window-size=1920,1080")  #1920x1080
    browser = webdriver.Chrome("C:/Users/dawid/PycharmProjects/FlaskProject/chromedriver.exe", options=op)
    browser.get(path)
    #browser.implicitly_wait(7)
    browser.find_element(By.XPATH, "//*[contains(text(), 'I Accept')]").click()
    #browser.implicitly_wait(10)
    time.sleep(3)
    browser.find_element(By.XPATH, "//*[@id='calendarMenu']").click()
    #browser.implicitly_wait(10)
    time.sleep(5)
    browser.find_elements(By.CLASS_NAME, "calendar__listItem")[deltaDate+7].click()
    #browser.implicitly_wait(10)
    time.sleep(5)
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(5)
    elements = browser.find_elements(By.XPATH,
                                     '//div[@class="event__match event__match--scheduled event__match--twoLine"]')
    browser.implicitly_wait(20)
    counter = 0
    matches = []  # (name, [courses home], [courses away], [courses draw])
    for element in elements:
        if counter > 3:
            break
        browser.execute_script("arguments[0].click();", element)
        browser.implicitly_wait(10)
        browser.switch_to.window(browser.window_handles[-1])
        browser.implicitly_wait(10)
        Odds_click = browser.find_element(By.XPATH, "//*[contains(text(), 'Odds')]")
        browser.execute_script("arguments[0].click();", Odds_click)
        odds = browser.find_elements(By.CLASS_NAME, 'oddsCell__odd')
        matches.append([browser.title])
        matches[counter].append([])
        matches[counter].append([])
        matches[counter].append([])
        matches[counter].append(0)
        licznik = 0
        for odd in odds:
            if licznik % 3 == 0:
                matches[counter][1].append(odd.get_attribute("title"))
            elif licznik % 3 == 1:
                matches[counter][2].append(odd.get_attribute("title"))
            else:
                matches[counter][3].append(odd.get_attribute("title"))
            licznik += 1
        counter += 1
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    #browser.implicitly_wait(5)
    browser.close()
    stringCut(matches)
    probability(matches)
    df = pd.DataFrame(matches, columns=['Match', 'Home', ' Draw', 'Away', 'Probabilities'])
    return df


def stringCut(arr):
    key = '»'
    for i in range(len(arr)):
        for j in range(1, 4):
            arr[i][j] = list(filter(lambda x: x != '', arr[i][j]))
            for k in range(len(arr[i][j])):
                if key in arr[i][j][k]:
                    arr[i][j][k] = arr[i][j][k][7:]
                    arr[i][j][k] = float(arr[i][j][k])

def probability(arr):
    for i in range(len(arr)):
        probab = 0
        for j in range(1,4):
            if len(arr[i][j]) != 0:
                probab += 1/(max(arr[i][j]))
        arr[i][4] = str(math.floor(probab*100)) + str(" %")


