from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Sports.enum_sports import  SportEnum
from models import  engine
from sqlalchemy.orm import sessionmaker

def open_page_to_list_matches(path, selectDate, deltaDate , amount, sport ):

    op = webdriver.ChromeOptions()
    op.add_argument('--disable-images')
    op.add_argument('headless')
    op.add_argument('--disable-javascript')
    op.add_argument("window-size=1920,1080")
    browser = webdriver.Chrome("chromedriver.exe", options=op)
    browser.get(path + sport.lower())

    elements = []
    try:
        WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "I Accept")]'))).click()

        WebDriverWait(browser,10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='calendarMenu']"))).click()

        WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar__listItem")))

        browser.find_elements(By.CLASS_NAME, "calendar__listItem")[deltaDate+7].click()

        browser.switch_to.window(browser.window_handles[-1])
        WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.XPATH,
                                             '//div[@class="event__match event__match--scheduled event__match--twoLine"]')))
        elements = browser.find_elements(By.XPATH,
                                             '//div[@class="event__match event__match--scheduled event__match--twoLine"]')
    except:
        print('Failed to load matches')
    counter = 0
    for element in elements:
        if counter >= amount:
            break
        Session = sessionmaker(bind=engine)
        session = Session()
        match, id_match, old_match = None, None, None
        try:
            id_match = element.get_attribute("id")
        except:
            print('Failed to get id matches')
        for val in SportEnum:
            if sport ==val.value:
                match = val.sport_object(id_match)
                session.query(val.db).filter(val.db.id_match == id_match).delete()
                break
        match.date = selectDate
        try:
            browser.execute_script("arguments[0].click();", element)
        except:
            print('The item cannot be clicked')
        browser.implicitly_wait(10)
        browser.switch_to.window(browser.window_handles[-1])
        browser.implicitly_wait(10)
        Odds_click = 0

        try:
            Odds_click = browser.find_elements(By.XPATH, "//*[contains(text(), 'Odds')]")
        except:
            print('There is no odds button')
        if len(Odds_click) > 1:
            try:
                browser.execute_script("arguments[0].click();", Odds_click[0])
            except:
                print('Script cannot be executed')
        else:
            browser.switch_to.window(browser.window_handles[0])
            session.commit()
            continue
        odds = browser.find_elements(By.CLASS_NAME, 'oddsCell__odd')
        match.match_name = browser.title
        mod_ = 0
        for odd in odds:
            match.sequence_on_page(mod_, odd.text)
            mod_ +=1
        match.set_probabilities()
        session.add(match.add_to_database())
        counter += 1
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        session.commit()
    browser.close()