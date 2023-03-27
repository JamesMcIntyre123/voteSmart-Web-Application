import re
from flask import Flask, render_template, url_for, make_response, request, redirect, session
#import pdfkit
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from quiz import PopQuiz, CheckAnswer, printScore
import sqlite3
import logging
import matplotlib.pyplot as plt
from flask_wtf.csrf import CSRFProtect
from candidate import StateQuiz, printCandidate
from pollLocation import printLocation



logging.basicConfig(filename='record.log', level=logging.DEBUG)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/aakritishah/Desktop/user_data.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign-Up")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose another one."
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class LocationForm(FlaskForm):
    city = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "City"})
    county = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "County"})
    state = StringField(validators=[InputRequired(), Length(min=2, max=2)], render_kw={"placeholder": "State (abbreviated)"})
    search = SubmitField("Search Poll Locations")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exit')
def exit():
    if session:
        session.clear()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    msg = ''
    form = LoginForm()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        app.logger.info("loginpage function called")
        con = sqlite3.connect("user_data.db")
        cursor = con.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [username, password])
        con.commit()

        user = cursor.fetchone()
        if user:
            session["name"] = user[1]
            session["id"] = user[0]
            return render_template('account.html', name=username)
        else:
            return render_template('nologin.html')
    return render_template('login.html', msg=msg, form=form)

@app.route('/history', methods=['GET', 'POST'])
def historypage():
        app.logger.info("history function called")
        if session:
            con = sqlite3.connect("user_data.db")
            cursor = con.cursor()
            cursor.execute('SELECT * FROM quizHistory WHERE user_id = ?', [session["id"]])
            #con.commit()

            history = cursor.fetchall()
            if history:
                name = session["name"]
                app.logger.info("history is found called %s , %d , %s",name, len(history), session["id"])
                return render_template('quizHistory.html', history=history, name=name)
            else:
                name = session["name"]
                app.logger.info("history not found %s %s",name, session["id"])
                return render_template('quizHistory.html', name=name)
        else:
            return render_template('nologin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signuppage():
    msg = ''
    form = RegisterForm()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        app.logger.info("signuppage function called")
        username = request.form['username']
        password = request.form['password']
        app.logger.info('%s username',username)
        con = sqlite3.connect("user_data.db")
        cursor = con.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', [username])
        con.commit()
        user = cursor.fetchone()
        if user:
            return render_template('signuperror.html', form=form)
        elif not username or not password:
            return render_template('signuperror.html', form=form)
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (:username, :password)', [username, password])
            con.commit()
            msg = 'You have successfully registered!'
            form = LoginForm()
            return render_template('signedup.html', form=form)
    return render_template('signup.html', form=form, msg=msg)

@app.route('/findpoll', methods=['GET', 'POST'])
def findpollpage():
    form = LocationForm()
    return render_template('findpoll.html', form=form)

@app.route('/location', methods=['GET', 'POST'])
def location():
    form = printLocation(request.form)
    
    if form.county != 0:
        county = form.county
        zip = form.zip
        streetnum = form.streetnum
        streetname = form.streetname
        state = form.state
        precinct = form.precinct
        city = form.city
        name = form.name
        site = form.site
    else:
        form = LocationForm()
        return render_template('findpoller.html', form=form)

    return render_template('location.html', county=county, zip=zip, state=state, streetnum=streetnum, streetname=streetname, name=name, precinct=precinct, city=city, site=site)


@app.route('/takequiz', methods=['GET','POST'])
def takequizpage():
    form = PopQuiz()
    #cand = candidateScore(request.form)
    #candidates = cand.candidates
    #score = CheckAnswer().printScore
    #app.logger.info("checkanswer function called")
    return render_template('quiz.html', form=form)


@app.route('/cand1')
def candidate1():
    form = printScore(request.form)
    district = form.dist1
    con = sqlite3.connect("user_data.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM candidates WHERE district = ?', [district])
    con.commit()
    cand = cursor.fetchall()
    name1 = cand[0][0]
    state1 = cand[0][3]
    party1 = cand[0][1]
    run1 = cand[0][4]
    bio1 = cand[0][2]
    dist1 = cand[0][5]
    site1 = cand[0][6]
    return render_template('repcand1.html', name1=name1, bio1=bio1, state1=state1, party1=party1, run1=run1, dist1=dist1, site1=site1)




@app.route('/val')
def val():
    name = "Val Demings"
    con = sqlite3.connect("user_data.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM candidates WHERE name = ?', [name])
    con.commit()
    cand = cursor.fetchone()
    state = cand[3]
    party = cand[1]
    run = cand[4]
    bio = cand[2]
    site = cand[6]
    app.logger.debug(bio)
    return render_template('cand.html', name=name, bio=bio, state=state, party=party, run=run, site=site)

@app.route('/marco')
def marco():
    name = "Marco Rubio"
    con = sqlite3.connect("user_data.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM candidates WHERE name = ?', [name])
    con.commit()
    cand = cursor.fetchone()
    state = cand[3]
    party = cand[1]
    run = cand[4]
    bio = cand[2]
    site = cand[6]
    app.logger.debug(bio)
    return render_template('cand.html', name=name, bio=bio, state=state, party=party, run=run, site=site)

@app.route('/charlie')
def charlie():
    name = "Charlie Crist"
    con = sqlite3.connect("user_data.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM candidates WHERE name = ?', [name])
    con.commit()
    cand = cursor.fetchone()
    state = cand[3]
    party = cand[1]
    run = cand[4]
    bio = cand[2]
    site = cand[6]
    app.logger.debug(bio)
    return render_template('cand.html', name=name, bio=bio, state=state, party=party, run=run, site=site)

@app.route('/ron')
def ron():
    name = "Ron Desantis"
    con = sqlite3.connect("user_data.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM candidates WHERE name = ?', [name])
    con.commit()
    cand = cursor.fetchone()
    state = cand[3]
    party = cand[1]
    run = cand[4]
    bio = cand[2]
    site = cand[6]
    app.logger.debug(bio)
    return render_template('cand.html', name=name, bio=bio, state=state, party=party, run=run, site=site)




@app.route('/results',methods=['GET','POST'])
def resultspage():
    #for fieldname, value in request.form.data.items:
    #        app.logger.debug("%s : %s", fieldname, value)
    form = printScore(request.form)

    right = form.right
    left = form.left
    ind = form.ind
    site1 = form.site1
    site2 = form.site2
    rotatec1 = int(form.rotatecand1)
    rotatec2 = int(form.rotatecand2)
    c1name = form.cand1
    c2name = form.cand2
    cand1score = form.cand1score
    cand2score = form.cand2score
    rscore = form.rightscore
    lscore = form.leftscore
    iscore = form.indscore
    dist = form.dist1

    rotatev = form.rotateval
    rotatem = form.rotatemarc
    rotatec = form.rotatechar
    rotater = form.rotateron
    # senators
    sen1 = form.valalign
    sen2 = form.marcalign

    # governers
    gov1 = form.charalign
    gov2 = form.ronalign

    con = sqlite3.connect("user_data.db")
    cursor = con.cursor()
    if session:
        cursor.execute('INSERT INTO quizHistory (user_id, rightscore, leftscore, indscore) VALUES (:user_id, :rscore, :lscore, :iscore)', [session["id"], rscore, lscore, iscore])
        con.commit()
    app.logger.debug(rotatec1)
    app.logger.debug(rotatec2)
    
    return render_template('aligns.html', rscore=rscore, lscore=lscore, iscore=iscore, sen1=sen1, sen2=sen2, gov2=gov2, gov1=gov1, rotatev=rotatev, rotatem=rotatem, rotater=rotater, rotatec=rotatec, rotatec1=rotatec1, rotatec2=rotatec2, c1name=c1name, c2name=c2name, cand1score=cand1score, cand2score=cand2score, dist=dist, site1=site1, site2=site2)
    
if __name__ == '__main__':
    app.run(debug=True)