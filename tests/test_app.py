import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app
from pymongo import MongoClient
from app import products_collection

MONGODB_URI = os.getenv('MONGODB_URI')

# Fixture to provide Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Fixture to provide MongoDb
@pytest.fixture
def mongodb_client():
    client = MongoClient(MONGODB_URI)
    db = client.shop_db
    yield db
    client.close()

#Test 1: Route Access Test
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200

#Test 1: Route Access Test
def test_products_route(client):
    response = client.get('/products')
    assert response.status_code == 200

# Test 2: Database Read Operation (MongoDB Ping)
def test_mongodb_connection(mongodb_client):
    """
    Test MongoDB read operation (ping the database to verify connection)
    """
    client = mongodb_client.client
    try:
        # Ping MongoDB to verify connection
        client.admin.command('ping')
        response = True
    except Exception as e:
        response = False
    
# Test 3: Database Write Operation (Insert Document)
def test_insert_document(mongodb_client):
    collection = mongodb_client.test_collection  # Replace with your actual collection name

    # Insert a test document
    test_data = {"name": "Test Document", "value": 123}
    insert_result = collection.insert_one(test_data)

    # Query the document
    found_document = collection.find_one({"name": "Test Document"})
    assert found_document is not None  # Ensure document was found
    assert found_document["value"] == 123  # Ensure the value is correct

        # Clean up
    collection.delete_one({"_id": insert_result.inserted_id})
