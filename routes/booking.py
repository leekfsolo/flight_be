from fastapi import APIRouter, Header
from schemas.user import serializeDict, serializeList
from models.booking import Booking
from config.db import db
from bson import ObjectId
from provider.authProvider import get_userId_from_request
import datetime

booking = APIRouter()

@booking.get('')
async def get_all_booking(Authorization: str = Header(default=None)):
  userId = get_userId_from_request(Authorization)
  bookings = serializeList(db.booking.aggregate([{
            '$match': {
              'userId': userId,
            }  
          },{
            '$lookup': {
                'from': 'tickets', 
                'localField': 'ticketId', 
                'foreignField': '_id', 
                'as': 'items'
            }
        }]))
  bookingData = []
  for booking in bookings:
    booking['ticketId'] = str(booking['ticketId'])
    booking.pop('userId')
    booking['items'] = [serializeDict(item) for item in booking['items']][0]
    bookingData.append(booking)
    
  return {'success': True, 'data': bookingData}

@booking.get('/{id}')
async def get_booking_detail(id):
  return serializeDict(db.booking.find_one({'_id': ObjectId(id)}))

@booking.post('')
async def add_booking(booking: Booking, Authorization: str = Header(default=None)):
  userId = get_userId_from_request(Authorization)
  bookingData = dict(booking)
  bookingData['ticketId'] = ObjectId(booking.ticketId)
  bookingData['userId'] = userId
  bookingData['created_at'] = datetime.datetime.now()
  db.booking.insert_one(bookingData)
  return {'success': True, 'message': 'Booking added successfully'}

@booking.delete('/{id}')
async def delete_booking(id):
  return serializeDict(db.booking.find_one_and_delete({'_id': ObjectId(id)}))