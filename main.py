from flask import Flask, request, redirect, render_template
import cgi
import os
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True

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
    else:
        title = response['Title']
        plot = response['Plot']
        poster = response['Poster']

    return render_template('search.html', title=title, plot=plot, poster=poster)

app.run()