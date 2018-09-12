# TODO: implement One to Many for User to Watchlist
# TODO: make Watchlist pull live data (only need title in db)
# TODO: give search an autocomplete function
# TODO: make search search exact title (done), and also similar titles
# TODO: look into web-hosting
# TODO: find release date info
# TODO: BOOTSTRAP
# TODO: add password hash
# TODO: contact Guidebox and workout access

from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://omdb:omdb@localhost:8889/omdb'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'U6JtITN8Qc'

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Title(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    plot = db.Column(db.String(1000))
    rating = db.Column(db.String(10))
    poster = db.Column(db.String(2064))

    def __init__(self, title, plot, rating, poster):
        self.title = title
        self.plot = plot
        self.rating = rating
        self.poster = poster
    

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        title = request.form['title']
        plot = request.form['plot']
        poster = request.form['poster']
        rating = request.form['rating']

        existing_title = Title.query.filter_by(title=title).first()
        if not existing_title:
            new_title = Title(title, plot, rating, poster)
            db.session.add(new_title)
            db.session.commit()

        return redirect('/watchlist')

    else:
        title = request.args.get('title')
        base_url = 'http://www.omdbapi.com/?apikey=111c0be2&plot=full&t='
        url = base_url + title
        response = requests.get(url).json()
        if response['Response'] == "False":
            title = "We're sorry, we couldn't find what you were looking for."
            plot = ''
            rating = 0
            poster = None
        else:
            title = response['Title']
            plot = response['Plot']
            rating = response['imdbRating']
            poster = response['Poster']

        return render_template('search.html', title=title, plot=plot, poster=poster, rating=rating)

@app.route("/account")
def account():
    users = User.query.all()
    return render_template('account.html', users=users)

@app.route("/watchlist", methods=['GET', 'POST'])
def watchlist():
    
    titles = Title.query.all()
    return render_template('watchlist.html', titles=titles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = ''
    email = ''
    password = ''
    username_error = ''
    email_error = ''
    password_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/watchlist')
        elif user:
            if user.password != password:
                password_error = 'Incorrect Password'
                password = ''
                return render_template('login.html', 
                    username = username,
                    password=password,
                    username_error = username_error,
                    password_error=password_error)
        elif not user:
            username_error = 'user does not exist'
            return render_template('login.html', 
                    username = username, 
                    password=password,
                    username_error=username_error,
                    password_error=password_error)
    else:
        return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        username_error = ''
        email_error = ''
        password_error = ''
        verify_error = ''

        if len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = "That's not a valid username"

        if len(email) < 3 or len(email) > 50 or ' ' in email or '@' not in email or '.' not in email:
            email_error = "That's not a valid email"
        
        if len(password) < 3 or len(password) > 20 or ' 'in password:
            password_error = "That's not a valid password"

        if verify != password:
            verify_error = "Passwords don't match"
            verify = ''
        
        if password_error:
            password = ''

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            username_error = 'Sorry, we already have a user under that name.'

        if username_error or email_error or password_error or verify_error:
            return render_template('signup.html',
                username=username,
                username_error=username_error,
                email=email,
                email_error=email_error,
                password=password,
                password_error=password_error,
                verify=verify,
                verify_error=verify_error)

        
        if not existing_user:
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/watchlist')

    return render_template('signup.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' not in session:
        return redirect('/')
    else:
        del session['username']
        return redirect('/')


if __name__ == '__main__':
    app.run()