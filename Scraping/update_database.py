from models import engine
from Sports.enum_sports import SportEnum
from sqlalchemy.orm import sessionmaker
import datetime
from Scraping.scrap_flashscore import open_page_to_list_matches

TODAY = datetime.date.today()

from datetime import datetime, timedelta

def delete_old_matches():
    Session = sessionmaker(bind=engine)
    session = Session()
    for sport in SportEnum:
        db = sport.db
        session.query(db).filter(db.date < TODAY).delete(synchronize_session=False)
    session.commit()


def upload_matches():
    for day in range(8):
        date = TODAY + timedelta(days=day)
        print(date)
        for sport in SportEnum:
            print(datetime.now())
            open_page_to_list_matches('https://www.flashscore.com/', date , day, 40, sport.value)
