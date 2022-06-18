# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

# Use flask-pymongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home(): 

    # Find one record of data from the mongo database and return it
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    
    # Create a Mars database
    mars_info = mongo.db.mars
    # Call the scrape function in the scrape_mars file which will scrape and save to mongo
    mars_scrape = scrape()
    # Update database with data being scraped
    mars_info.update_one({}, {"$set": mars_scrape}, upsert=True)

    # if mars:
    #     mars_table.update_one({"_id":mars["_id"]},{"$set": mars_data},upsert=True)
    # else:
    #     mars_table.insert_one(mars_data)

    # Redirect back to home page and return a message to show it was succesful
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
