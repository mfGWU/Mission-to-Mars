# Import dependencies
# First line says that we'll use Flask to render a template.
# Second line says we'll use PyMongo to interact with our Mongo database.
# Last line says that to use the scraping code, we will convert from Jupyter notebook to Python.

from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a 
#       uniform resource identifier similar to a URL.
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
#       This URI is saying that the app can reach Mongo through our localhost server, using port 27017, 
#       using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#  Set up our Flask routes: one for the main HTML page everyone will view when visiting the web app, 
#      and one to actually scrape new data using the code we've written.
#  Define the route for the HTML page Function
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)



#   function will set up our scraping route. This route will be the "button" of the web application, 
#   the one that will scrape updated data when we tell it to from the homepage of our web app. 
#  Now that we've gathered new data, we need to update the database using 
#    .update(). Let's take a look at the syntax we'll use
#   It'll be tied to a button that will run the code when it's clicked.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"


# Need for Flask is to tell it to run
if __name__ == "__main__":
   app.run()

