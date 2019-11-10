import scrape_mars
from flask import render_template, Flask
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)   

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars


@app.route('/scrape')
def scrape():
    info = scrape_mars.scrape()
    # drop duplicate info
    db.mars_info.drop()
    db.mars_info.insert_one(info)

    return 'Scraped!'

if __name__ == "__main__":
    app.run(debug=True)
