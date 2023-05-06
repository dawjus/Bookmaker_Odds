from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import pandas as pd
from Scraping.cleaningData import stringCut, probability
from models import Match, engine
from sqlalchemy.orm import sessionmaker
import time


def flashscore(path,selectDate, deltaDate =0, amount=5):
    Session = sessionmaker(bind=engine)
    session = Session()
    op = webdriver.ChromeOptions()
    op.add_argument('--disable-images')
    op.add_argument('headless')
    op.add_argument('--disable-javascript')
    op.add_argument("window-size=1920,1080")  #1920x1080
    browser = webdriver.Chrome("chromedriver.exe", options=op)
    browser.get(path)
    #browser.find_element(By.XPATH, "//*[contains(text(), 'I Accept')]").click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "I Accept")]'))
    ).click()
    WebDriverWait(browser,10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='calendarMenu']"))).click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar__listItem"))
    )
    browser.find_elements(By.CLASS_NAME, "calendar__listItem")[deltaDate+7].click()
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
        id_match = element.get_attribute("id")
        if session.query(Match).filter_by(id_match=id_match).count()>0:
            continue
        browser.execute_script("arguments[0].click();", element)
        browser.implicitly_wait(10)
        browser.switch_to.window(browser.window_handles[-1])
        browser.implicitly_wait(10)
        Odds_click = browser.find_elements(By.XPATH, "//*[contains(text(), 'Odds')]")
        if len(Odds_click) > 1:
            browser.execute_script("arguments[0].click();", Odds_click[0])
        else:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue
        #browser.execute_script("arguments[0].click();", Odds_click)
        odds = browser.find_elements(By.CLASS_NAME, 'oddsCell__odd')
        #matches.append([browser.title, [], [], [], 0])
        matches.append([browser.title,[], [], [], 0, id_match])
        mod_ = 0
        for odd in odds:
            if mod_ % 3 == 0:
                matches[counter][1].append(odd.get_attribute("title"))
            elif mod_ % 3 == 1:
                matches[counter][2].append(odd.get_attribute("title"))
            else:
                matches[counter][3].append(odd.get_attribute("title"))
            mod_ += 1
        stringCut(matches[counter])
        probability(matches[counter])
        match = Match(id_match=str(matches[counter][5]),name=str(matches[counter][0]),home=str(matches[counter][1]),
                      draw=str(matches[counter][2]), away=str(matches[counter][3]), probability=str(matches[counter][4]), date=selectDate)
        session.add(match)
        counter += 1
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    browser.close()
    session.commit()

    dbmatch = session.query(Match).filter_by(date = selectDate)

    #df = pd.DataFrame(matches, columns=['Match', 'Home', ' Draw', 'Away', 'Probabilities'])
    return createDataFrame(dbmatch)


def createDataFrame(database):
    data = {'Match': [match.name for match in database],
          'home': [match.home for match in database],
          'away': [match.away for match in database],
          'draw': [match.draw for match in database],
          'probability': [match.probability for match in database]
          }
    return pd.DataFrame(data)
