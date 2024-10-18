from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# MongoDB connection
app.config.from_prefixed_env('MYAPP')
client = MongoClient(app.config['CONNECTION_STRING'])
db = client.shop_db
products_collection = db.products

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    products = products_collection.find()
    return render_template('products.html',products=products)


if __name__ == '__main__':
    app.run(debug=True)