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
