from fastapi import APIRouter, Header, Depends
from schemas.user import serializeDict, serializeList
from models.booking import Booking
from config.db import db
from bson import ObjectId
from provider.jwtProvider import jwtBearer
from provider.authProvider import get_userId_from_request
from routes.ticket import get_ticket_detail
import datetime
from decouple import config
import httpx
import json
from .cart import handle_response

GHN_TOKEN = config('GHN_TOKEN')
GHN_SHOP_ID = config('GHN_SHOP_ID')
GHN_BASE_URL = "https://dev-online-gateway.ghn.vn/shiip/public-api/v2"
booking = APIRouter()


@booking.get('')
async def get_all_booking(Authorization: str = Header(default=None)):
    userId = get_userId_from_request(Authorization)
    bookings = serializeList(db.booking.aggregate([{
        '$match': {
            'userId': userId,
        }
    }, {
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
        booking['items'] = [serializeDict(item)
                            for item in booking['items']][0]
        bookingData.append(booking)

    return {'success': True, 'data': bookingData}


@booking.get('/{id}')
async def get_booking_detail(id):
    return serializeDict(db.booking.find_one({'_id': ObjectId(id)}))


@booking.post('', dependencies=[Depends(jwtBearer())])
async def add_booking(booking: Booking, Authorization: str = Header(default=None)):
    try:
        userId = get_userId_from_request(Authorization)
        bookingData = dict(booking)
        bookingData['ticketId'] = ObjectId(booking.ticketId)
        bookingData['userId'] = userId
        bookingData['created_at'] = datetime.datetime.now()
        db.booking.insert_one(bookingData)

        ticketData = await get_ticket_detail(booking.ticketId)

        async with httpx.AsyncClient(base_url=GHN_BASE_URL, headers={"ShopId": GHN_SHOP_ID, "Token": GHN_TOKEN, "Content-Type": "application/json"}) as client:
            data = {
                "required_note": "KHONGCHOXEMHANG",
                "payment_type_id": 2,
                "to_name": booking.email,
                "to_phone": booking.phone,
                "to_address": "268 Lý Thường Kiệt, Phường 14, Quận 10, Hồ Chí Minh, Vietnam",
                "to_ward_code": "21311",
                "to_district_id": 1461,
                "service_id": 100039,
                "service_type_id": 2,
                "weight": 200,
                "length": 20,
                "width": 5,
                "height": 2,
                "items": [
                    {
                        "name": ticketData["flightId"],
                        "code": booking.ticketId,
                        "quantity": 1,
                        "price": int(ticketData["price"]),
                        "weight": 200,
                    }
                ]
            }
            await client.post("/shipping-order/create", data=json.dumps(data))
        return {"success": True,
                "message": "Booking added successfully"}
    except Exception as error:
        print("Failed to create order:", error)


@booking.delete('/{id}')
async def delete_booking(id):
    return serializeDict(db.booking.find_one_and_delete({'_id': ObjectId(id)}))
