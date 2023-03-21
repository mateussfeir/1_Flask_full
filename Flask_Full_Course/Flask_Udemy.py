
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Using permanent_session_lifetime we are setting how long the page will log automatically in the last account logged.
app.permanent_session_lifetime = timedelta(minutes=5)

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

@app.route('/login', methods = ['POST', 'GET'])
def login(): 
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        session['user'] = user

        # users is the class model created above
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
                flash('Already logged in!')

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
The main purpose is to learn how to creat a UI where the user can input some information and receive a feedback
'''