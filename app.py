from flask import Flask,g, render_template_string, request, render_template, Response, redirect, session
import pandas as pd
from Scraping import scrapFlashscore, updateDataBase
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
from models import Football, engine
from sqlalchemy.orm import sessionmaker
import threading
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)
executor = ThreadPoolExecutor()
scraping_thread = None

app.secret_key = 'supersecretkey'
ALLOWED_EXTENSIONS = {'csv'}

@app.route('/', methods=[ 'GET','POST'])
def start():
    global scraping_thread
    if scraping_thread is None:
        scraping_thread = executor.submit(background_task)
    #print_matches()
    if request.method =='POST':
        selected_date = request.form.get('selected_date')
        sport = request.form.get('sport')
        amount = request.form.get('selected_amount')
        session['selected_date'] = selected_date
        session['sport'] = sport
        session['amount'] = amount
        return redirect('/matches')
    today = datetime.date.today().strftime('%Y-%m-%d')
    max_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    return render_template('temp.html', today=today, max_date=max_date)



@app.route('/matches', methods=['GET','POST'])
def matches():
    today = datetime.date.today()
    sport = session.get('sport')
    selectDateString = session.get('selected_date')
    amount = int(session.get('amount'))
    selectDate = datetime.datetime.strptime(selectDateString, '%Y-%m-%d').date()
    delta = (selectDate - today).days
    '''if 'Soccer' == sport: #request.form:
        df = scrapFlashscore.flashscore('https://www.flashscore.com',selectDate, delta, amount)
    elif 'Basketball' == sport:
        df = scrapFlashscore.flashscore('https://www.flashscore.com/basketball/',selectDate, delta, amount)
    elif 'Handball' == sport:
        df = scrapFlashscore.flashscore('https://www.flashscore.com/handball/', selectDate,delta, amount)
    else:
        df = 0
    session['df'] = df.to_json(orient='records')
    '''
    Session = sessionmaker(bind=engine)
    sesja = Session()
    database = sesja.query(Football).filter_by(date = selectDate)
    df = scrapFlashscore.getData(database, amount)
    html_string = df.to_html(classes='table table-striped', index=False)
    html_string = html_string.replace('<table',
                                          '<table style="background-color: lightblue; border: 2px solid black;"')
    html_string = html_string.replace('<tbody>', '<tbody style="background-color: white;">')

    return render_template('tables.html', tabela=html_string, tytul='d1')


def print_matches():
    Session = sessionmaker(bind=engine)
    session = Session()

    matches = session.query(Football).all()

    for match in matches:
        print(f"ID: {match.id}")
        print(f"Team 1: {match.name}")
        print(f"Team 2: {match.home}")
        print(f"Date: {match.draw}")
        print("---")


@app.route('/some_url', methods=['POST'])
def some_function():
    json_data  = session.get('df')
    df = pd.read_json(json_data)
    df.to_csv('data.csv', index=False)
    return 'Data saved to CSV'


def background_task():
    today = datetime.date.today()
    for i in range(7):
        print(i)
        print('----------------')
        selectDate = today + datetime.timedelta(days=i)
        updateDataBase.flashscore('https://www.flashscore.com',selectDate, i, 10)


if __name__ == '__main__':
    background_thread = threading.Thread(target=background_task)
    background_thread.start()
    app.run(debug=True)
