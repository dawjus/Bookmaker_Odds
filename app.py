from flask import Flask, render_template_string, request, render_template, Response
import pandas as pd
from Scraping import WebFlashscore
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
app = Flask(__name__)


@app.route('/', methods=[ 'GET','POST'])
def hello_world():
    print("jołek")
    today = datetime.date.today()
    if request.method =='POST':
        selectDateString = request.form.get('selected_date')
        selectDate = datetime.datetime.strptime(selectDateString, '%Y-%m-%d').date()
        delta = (selectDate - today).days
        if 'soccer' in request.form:
            df = WebFlashscore.flashscore('https://www.flashscore.com', delta)
        elif 'basketball' in request.form:
            df = WebFlashscore.flashscore('https://www.flashscore.com/basketball/', delta)
        elif 'handball' in request.form:
            df = WebFlashscore.flashscore('https://www.flashscore.com/handball/', delta)
        else:
            df = 0

        html_string = df.to_html(classes='table table-striped', index=False)
        html_string = html_string.replace('<table',
                                          '<table style="background-color: lightblue; border: 2px solid black;"')
        html_string = html_string.replace('<tbody>', '<tbody style="background-color: white;">')
        html_string = html_string.replace('<body>', '<body bgcolor="#FFFFCC">')
        return html_string

    today = datetime.date.today().strftime('%Y-%m-%d')
    max_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    return render_template('temp.html', today=today, max_date=max_date)



if __name__ == '__main__':
    app.run(debug=True)





