from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

# MongoDB connection
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

client = MongoClient(f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@devops.nxb7m.mongodb.net/?retryWrites=true&w=majority&appName=DevOps')
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