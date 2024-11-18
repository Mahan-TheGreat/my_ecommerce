import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app
from pymongo import MongoClient
from app import products_collection


MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_products_route(client):
    response = client.get('/products')
    assert response.status_code == 200


def test_mongo_connection():
    client = MongoClient(f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@devops.nxb7m.mongodb.net/?retryWrites=true&w=majority&appName=DevOps')
    result = client.admin.command('ping')
    assert result['ok'] == 1.0


def test_mongo_write():
    test_document = {'name': 'Test Product', 'price': 100}
    insert_result = products_collection.insert_one(test_document)

    # Verify the document exists
    retrieved_document = products_collection.find_one({'_id': insert_result.inserted_id})
    assert retrieved_document['name'] == 'Test Product'
    assert retrieved_document['price'] == 100

    # Cleanup
    products_collection.delete_one({'_id': insert_result.inserted_id})