from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from models import Football_db, Handball_db, engine, Basketball_db
from Sports.enum_sports import SportEnum
from sqlalchemy.orm import sessionmaker
import datetime
from Scraping.scrapFlashscore import open_page_to_list_matches


TODAY = datetime.date.today()

from datetime import datetime, timedelta

def delete_old_matches():
    Session = sessionmaker(bind=engine)
    session = Session()
    TOMORROW = datetime.now().date() + timedelta(days=1)
    for sport in SportEnum:
        db = sport.get_db()
        session.query(db).filter(db.date < TODAY).delete(synchronize_session=False)
    session.commit()


def upload_matches():
    for day in range(1,8):
        date = TODAY + timedelta(days=day)
        print(date)
        for sport in SportEnum:
            Session = sessionmaker(bind=engine)
            session = Session()
            open_page_to_list_matches('https://www.flashscore.com/', date , day, 3, sport.value)
            print("zmiana bociana")
            session.commit()
