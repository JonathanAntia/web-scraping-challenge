from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo set up a mongo connection
app.config['MONGO_URI'] = "mongodb://localhost:27017mission_to_mars_db"
mongo = PyMongo(app)


@app.route('/')
def index():
    collection = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data=collection)



@app.route('/scrape')
def scraper():
    collection = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    collection.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__"
    app.run(debug=True)