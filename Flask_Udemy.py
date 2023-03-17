
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'hello'
# Using permanent_session_lifetime we are setting how long the page will log automatically in the last account logged.
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
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
        return f"<h1>{'User: ' + user}</h1>"
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f'You have been logged out! {user}', 'info')
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/new')
def test():
    return render_template('new.html')


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
The main purpose is to learn how to creat a UI where the user can input some information and receive a feedback
'''
