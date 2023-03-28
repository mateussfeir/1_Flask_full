
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd

app = Flask(__name__)
app.secret_key = 'hello'

# SQLAlchemy allows devs to define database models using Python classes, rather than writing raw SQL.
# It's just like a shortcut

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Using permanent_session_lifetime we are setting how long the page will log automatically in the last account logged.

app.permanent_session_lifetime = timedelta(minutes=5)

# Routes available:
# / - Welcome page      
# /login - Allows the user to input his name and e-mail to create his account
# /user - If not logged, redirect to the login page. If logged shows the e-mail saved
# /logout - Logout
# /view - Shows all of the names and e-mails saved on the database
# /new - Route test
# /return_simulator - Asks the user to input the company and shows the real time price


db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html', values = users.query.all())

@app.route('/login', methods = ['POST', 'GET'])
def login(): 
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        # we use session (imported from flask library) to store informations
        session['user'] = user

        # users is the class model previous created
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
 
        flash('Login Succesful!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already logged in!')
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    # If logged return User: 'Already logged'
    email = None
    if 'user' in session:
        user = session['user']

        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash('Email was saved!')
        else:
            if 'email' in session:
                email = session['email']
                flash('User already logged in!')

        return render_template('user.html', email=email)
    # If not logged, redirect to the login page
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash(f'You have been logged out!', 'info')
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/simulator', methods = ['POST', 'GET'])
def simulate():
    if request.method == 'POST':
        flash(f'Welcome to the return simulator page.')
        session.permanent = True
        stock = request.form['stock']
        session['stock'] = stock
        money = request.form['money']
        session['money'] = money
        date = request.form['date']
        session['date'] = date

        # 1) Specify API endpoint and parameters

        url = 'https://www.alphavantage.co/query'
        params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': stock,
        'outputsize': 'full',
        'apikey': 'TE1E1KD330UYLRHQ'
        }

        # 2) Make API request and retrieve data

        response = requests.get(url, params=params)
        data = response.json()

        # 3) Check if the asset was opened for trade at the day, in this case we are going to check if
        # the date is in the provided list


        date = request.form['date']

        # 4) Convert data to Pandas DataFrame

        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)

        # 5) Get the stock price for a specific date

        old_price = df.loc[date]['5. adjusted close']
        session['old_price'] = round(old_price, 2)
        new_price = df.iloc[0]['4. close']
        session['new_price'] = round(new_price, 2)
        percentage_return = round((1 - new_price/old_price)*100, 2)
        session['percentage_return'] = percentage_return
        fmoney = float(money)
        actual_value = (fmoney + (fmoney*(percentage_return/100)))
        session['actual_value'] = actual_value
        profit_loss = actual_value - fmoney
        session['profit_loss'] = profit_loss

        return render_template('simulator.html', stock = session['stock'], money = session['money'], date = session['date'], old_price = session.get('old_price'), new_price = session.get('new_price'), percentage_return = session.get('percentage_return'), actual_value = session.get('actual_value'), profit_loss = session.get('profit_loss'))
    else: 
        return render_template('simulator.html')


@app.route('/price', methods = ['POST', 'GET'])
def price():
    if request.method == 'POST':
        session.permanent = True
        stock = request.form['stock']
        session['stock'] = stock
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': stock,
            'outputsize': 'full',
            'apikey': 'TE1E1KD330UYLRHQ'
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        price = df.iloc[0]['4. close']
        session['price'] = price
        if 'stock' in session:
            return render_template('price.html', stock=session['stock'], data=session.get('price', ""))
        else:
            return redirect(url_for('index'))
    return render_template('price.html')
    
@app.route('/new')
def test():
    return render_template('new.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port= 8080)


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
The main purpose is to learn how to creat an UI where the user can input some information and receive a feedback
'''