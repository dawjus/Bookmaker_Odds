from flask import Flask, g, render_template_string, request, render_template, Response, redirect, session
import pandas as pd
from Scraping import update_database
import datetime
from models import Football_db, engine, Basketball_db
from Sports.enum_sports import SportEnum
from sqlalchemy.orm import sessionmaker
import threading
from concurrent.futures import ThreadPoolExecutor
from Scraping.sure_bets import sure_bets

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

    if request.method == 'POST':
        if 'sport' in request.form:
            selected_date = request.form.get('selected_date')
            sport = request.form.get('sport')
            amount = request.form.get('selected_amount')
            session['selected_date'] = selected_date
            session['sport'] = sport
            session['amount'] = amount
            return redirect('/matches')
        elif 'surebets' in request.form:
            return redirect('/surebets')

    today = datetime.date.today().strftime('%Y-%m-%d')
    max_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    return render_template('temp.html', today=today, max_date=max_date)



@app.route('/matches', methods=['GET','POST'])
def matches():
    sport_val = session.get('sport')
    selectDateString = session.get('selected_date')
    amount = int(session.get('amount'))
    selectDate = datetime.datetime.strptime(selectDateString, '%Y-%m-%d').date()
    db, sport_object = None, None
    for sport in SportEnum:
        if sport.value == sport_val:
            db = sport.db
            sport_object = sport.sport_object
            break
    df = sport_object.create_data_frame(db, amount, selectDate)

    session['df'] = df.to_json(orient='records')
    html_string = df.to_html(classes='table table-striped', index=False,  escape=False, render_links=True)
    html_string = html_string.replace('<table',
                                          '<table style="background-color: lightblue; border: 2px solid black;"')
    html_string = html_string.replace('<tbody>', '<tbody style="background-color: white;">')
    html_string = html_string.replace('<td>{{ row[\'URL\'] }}</td>', '<td><a href="{{ row[\'URL\'] }}">{{ row[\'URL\'] }}</a></td>')
    return render_template('tables.html', tabela=html_string, tytul='d1',)


@app.route('/surebets', methods=['GET', 'POST'])
def surebets():
    df = sure_bets()
    html_string = df.to_html(classes='table table-striped', index=False,  escape=False, render_links=True)
    html_string = html_string.replace('<table',
                                          '<table style="background-color: lightblue; border: 2px solid black;"')
    html_string = html_string.replace('<tbody>', '<tbody style="background-color: white;">')
    html_string = html_string.replace('<td>{{ row[\'URL\'] }}</td>', '<td><a href="{{ row[\'URL\'] }}">{{ row[\'URL\'] }}</a></td>')
    return render_template('tables.html', tabela=html_string, tytul='d1',)


def background_task():
    while(True):
        update_database.delete_old_matches()
        update_database.upload_matches()


if __name__ == '__main__':
    background_thread = threading.Thread(target=background_task)
    background_thread.start()
    app.run(debug=True)
