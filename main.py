from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
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

class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))

    def __init__(self, title):
        self.title = title
    

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def search():
    title = request.args.get('title')
    base_url = 'http://www.omdbapi.com/?apikey=111c0be2&t='
    url = base_url + title
    response = requests.get(url).json()
    if response['Response'] == "False":
        title = "something we couldn't find"
        plot = "Sorry, your entry was not recognized."
        rating = 0
        poster = None #Image.open("C:\Users\Jonathan\Documents\00_Scratch\omdb\static\images\sadimirPutin.jpg")
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

if __name__ == '__main__':
    app.run()