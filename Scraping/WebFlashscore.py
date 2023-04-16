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
import re

def flashscore(path='https://www.flashscore.com', deltaDate =0, amount=5):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument("window-size=1920,1080")  #1920x1080
    browser = webdriver.Chrome("C:/Users/dawid/PycharmProjects/FlaskProject/chromedriver.exe", options=op)
    browser.get(path)
    #browser.find_element(By.XPATH, "//*[contains(text(), 'I Accept')]").click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "I Accept")]'))
    ).click()
    WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='calendarMenu']"))).click()
    #browser.find_element(By.XPATH, "//*[@id='calendarMenu']").click()
    #browser.implicitly_wait(10)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar__listItem"))
    )
    browser.find_elements(By.CLASS_NAME, "calendar__listItem")[deltaDate+7].click()
    #browser.implicitly_wait(10)
   # time.sleep(5)
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.XPATH,
                                     '//div[@class="event__match event__match--scheduled event__match--twoLine"]')))
    elements = browser.find_elements(By.XPATH,
                                     '//div[@class="event__match event__match--scheduled event__match--twoLine"]')

    counter = 0
    matches = []  # (name, [courses home], [courses away], [courses draw])
    for element in elements:
        if counter >= amount:
            break
        browser.execute_script("arguments[0].click();", element)
        browser.implicitly_wait(10)
        browser.switch_to.window(browser.window_handles[-1])
        browser.implicitly_wait(10)
        #Odds_click = browser.find_element(By.XPATH, "//*[contains(text(), 'Odds')]")
        Odds_click = browser.find_elements(By.XPATH, "//*[contains(text(), 'Odds')]")
        if len(Odds_click) > 1:
            browser.execute_script("arguments[0].click();", Odds_click[0])
        else:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue
        #browser.execute_script("arguments[0].click();", Odds_click)
        odds = browser.find_elements(By.CLASS_NAME, 'oddsCell__odd')
        matches.append([browser.title, [], [], [], 0])
        mod_ = 0
        for odd in odds:
            if mod_ % 3 == 0:
                matches[counter][1].append(odd.get_attribute("title"))
            elif mod_ % 3 == 1:
                matches[counter][2].append(odd.get_attribute("title"))
            else:
                matches[counter][3].append(odd.get_attribute("title"))
            mod_ += 1
        counter += 1
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    browser.close()
    stringCut(matches)
    probability(matches)
    df = pd.DataFrame(matches, columns=['Match', 'Home', ' Draw', 'Away', 'Probabilities'])
    return df


def stringCut(arr):
    for i in range(len(arr)):
        for j in range(1, 4):
            arr[i][j] = list(filter(lambda x: x != '', arr[i][j]))
            for k in range(len(arr[i][j])):
                arr[i][j][k] = re.findall(r'\d+\.\d+', arr[i][j][k])
                if len(arr[i][j][k]) >1:
                    arr[i][j][k] = float(arr[i][j][k][1])
                else:
                    arr[i][j][k] =-1

def probability(arr):
    for i in range(len(arr)):
        probab = 0
        for j in range(1,4):
            if len(arr[i][j]) != 0:
                probab += 1/(max(arr[i][j]))
        arr[i][4] = str(math.floor(probab*100)) + str(" %")


