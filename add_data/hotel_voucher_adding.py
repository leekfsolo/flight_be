import datetime
import random
from faker import Faker
import certifi
from pymongo import MongoClient

uri = "mongodb+srv://leekfsolo:Kennguyen0309@flight-booking.ockhllv.mongodb.net/?retryWrites=true&w=majority"

conn = MongoClient(uri, tlsCAFile=certifi.where())

try:
    conn.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = conn.flight_booking

fake = Faker()

def convert_to_datetime(date_obj):
    return datetime.datetime.combine(date_obj, datetime.datetime.min.time())

# Example data for products (clothes, books, smartphones) with simple random image URLs
def run():
    example_products = [
        {
            'productCode': fake.uuid4(),
            'expirationDate': convert_to_datetime(fake.future_date()),
            'numberOfProduct': random.randint(1, 100),
            'status': random.choice(['Active', 'Inactive']),
            'originalPrice': round(random.uniform(50, 500), 2),
            'salePrice': 0,  # Initialize salePrice to 0
            'category': random.choice(['Clothes', 'Books', 'Smartphones']),
            'brand': fake.company(),
            'location': fake.city(),
            'description': fake.paragraphs(nb=random.randint(4, 6)),  # Adjust as needed
            'image': f'https://picsum.photos/seed/{i}/500/300',
        }
        for i in range(1, 21)
    ]

    for product in example_products:
        # Ensure salePrice is lower than originalPrice
        product['salePrice'] = round(random.uniform(30, product['originalPrice']), 2)

    products_collection = db["voucher"]

    # Insert the example product data
    products_collection.insert_many(example_products)

    # Print a confirmation message
    print("Example product data inserted into MongoDB.")

run()
