
from flask import Flask, redirect, url_for, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'hello'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form["nm"]
        session['user'] = user
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return f'<h1>{user}</h1>'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logoout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/new')
def test():
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True, port= 8080)









# @app.route('/price', methods=['GET'])

# def get_price():
#     # ticker = request.form['ticker']
#     url = 'https://www.alphavantage.co/query'
#     params = {'function': 'TIME_SERIES_DAILY_ADJUSTED', 
#             # 'symbol': ticker.upper(),
#             'symbol': 'TSLA',
#             'apikey': 'TE1E1KD330UYLRHQ'}  
#     response = requests.get(url, params=params)
#     data = response.json()
#     df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
#     df = df.astype(float)
#     df.index = pd.to_datetime(df.index)
#     new_price = df.iloc[0]['4. close']
#     # return 'Price for ' + ticker.uuper() + ': ' + str(new_price) + '$'
#     return 'Price:' + str(new_price) + '$'



''' 
Flask course from Udemy.

 There are 5 most important HTTP words:
 POST : Add data ('Secured information')
 GET : Retrieve Data ('Not secure, you do not care if someone sees it')
 DELETE : Remove Data
 PATCH : Update Data
 PUT : Replace Data

Data Formats: HTML and JSON

Goal of this code:
Make a webpage where the user can choose the company and receive the data related to its financial statement
(Specially the revenue and profit) or parhaps just even the price of a chosen stock.
The main purpose is to learn how to creat a UI where the user can input some information and receive a feedback
'''
