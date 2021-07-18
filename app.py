import re
from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)


@app.route("/")
def index():
    data = mongo.db.webscrapes.find_one()
    print(data)
    return render_template('index.html',data = data)


@app.route("/scrape")
def scrape():
    webscrapes_handle = mongo.db.webscrapes
    webscrape = scrape_mars.scrape()
    webscrapes_handle.update({}, webscrape, upsert=True)
    return redirect("/",code=302)

if __name__ == '__main__':
    app.run(debug=True)
