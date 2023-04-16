from flask import Flask, render_template_string, request, render_template, Response, redirect, session
import pandas as pd
from Scraping import WebFlashscore
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = 'supersecretkey'
ALLOWED_EXTENSIONS = {'csv'}

@app.route('/', methods=[ 'GET','POST'])
def start():
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
    if 'Soccer' == sport: #request.form:
        df = WebFlashscore.flashscore('https://www.flashscore.com', delta,  amount)
    elif 'Basketball' == sport:
        df = WebFlashscore.flashscore('https://www.flashscore.com/basketball/', delta,amount)
    elif 'Handball' == sport:
        df = WebFlashscore.flashscore('https://www.flashscore.com/handball/', delta, amount)
    else:
        df = 0
    session['df'] = df.to_json(orient='records')
    html_string = df.to_html(classes='table table-striped', index=False)
    html_string = html_string.replace('<table',
                                          '<table style="background-color: lightblue; border: 2px solid black;"')
    html_string = html_string.replace('<tbody>', '<tbody style="background-color: white;">')

    return render_template('tables.html', tabela=html_string, tytul='d1')




@app.route('/some_url', methods=['POST'])
def some_function():
    json_data  = session.get('df')
    df = pd.read_json(json_data)
    df.to_csv('data.csv', index=False)
    return 'Data saved to CSV'

if __name__ == '__main__':
    app.run(debug=True)





