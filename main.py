from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://omdb:omdb@localhost:8889/omdb'
app.config['SQLALCHEMY_ECHO'] = True

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

@app.route("/search")
def search():

        if request.method == 'GET':
            title = request.args.get('title')
            base_url = 'http://www.omdbapi.com/?apikey=111c0be2&plot=full&t='
            url = base_url + title
            response = requests.get(url).json()
            if response['Response'] == "False":
                title = "something we couldn't find"
                plot = "Sorry, your entry was not recognized."
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

    if request.method == 'POST':
        title = request.form['title']
        plot = request.form['plot']
        poster = request.form['poster']
        rating = request.form['rating']

        new_title = Title(title, plot, rating, poster)
        db.session.add(new_title)
        db.session.commit()
    
    titles = Title.query.all()
    return render_template('watchlist.html', titles=titles)

if __name__ == '__main__':
    app.run()