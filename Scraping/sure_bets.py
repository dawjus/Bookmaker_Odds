import pandas as pd
from Sports.enum_sports import  SportEnum
from models import  engine
from sqlalchemy.orm import sessionmaker


def sure_bets():
    Session = sessionmaker(bind=engine)
    session = Session()

    df_all = []
    for sport in SportEnum:
        db = session.query(sport.db).all()
        data = {'Sport': [sport.value for _ in db],
                'Match': [match.name for match in db],
                'Probability': [match.probability for match in db],
                'Date' : [match.date for match in db],
                'URL': [match.id_match[4:] for match in db]
                }
        df = pd.DataFrame(data)
        df['Probability'] = pd.to_numeric(df['Probability'], errors='coerce')
        df = df.dropna(subset=['Probability'])
        df['URL'] = df['URL'].apply(lambda x: f'<a href="https://www.flashscore.com/match/{x}">{"Match Details"}</a>')
        df_all.append(df)
    df_all = pd.concat(df_all, ignore_index=True)
    session.commit()
    return df_all.where(df_all['Probability']<1).dropna().sort_values('Probability')

