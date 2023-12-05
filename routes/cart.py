from pydantic import Field
from fastapi import APIRouter, Header, Depends, Body
from schemas.user import serializeDict, serializeList
from config.db import db
from bson import ObjectId
from provider.authProvider import get_userId_from_request
from provider.jwtProvider import jwtBearer
import datetime
import base64
from decouple import config
import httpx
from models.CustomBaseModels import CustomBaseModel

# PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
# PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"


class PaypalApprove(CustomBaseModel):
    orderId: str = Field(default=None)


async def handle_response(response, success=True, message=""):
    try:
        json_response = await response.json()
        return {
            "jsonResponse": json_response,
            "httpStatusCode": response.status_code,
            "success": success,
            "message": message
        }
    except Exception as err:
        error_message = await response.text()
        raise Exception(error_message)


async def generate_access_token():
    try:
        if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
            raise Exception("MISSING_API_CREDENTIALS")

        auth = base64.b64encode(
            f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()).decode()

        async with httpx.AsyncClient(base_url=PAYPAL_BASE_URL) as client:
            response = await client.post("/v1/oauth2/token", data="grant_type=client_credentials", headers={
                "Authorization": f"Basic {auth}"
            })

        data = response.json()
        return data["access_token"]
    except Exception as error:
        print("Failed to generate Access Token:", error)

cart = APIRouter()


@cart.get('', dependencies=[Depends(jwtBearer())])
async def get_all_cart_items(Authorization: str = Header(default=None)):
    try:
        userId = get_userId_from_request(Authorization)
        cartList = serializeList(db.cart.aggregate([
            {
                '$lookup': {
                    'from': 'tickets',
                    'localField': 'ticketId',
                    'foreignField': '_id',
                    'as': 'items'
                }
            }, {
                '$lookup': {
                    'from': 'user',
                    'localField': 'userId',
                    'foreignField': '_id',
                    'as': 'users'
                }
            }
        ]))

        myCartList = []
        for cart in cartList:
            if str(cart['userId']) == str(userId):
                for item in cart['items']:
                    item['id'] = str(item['_id'])
                    item.pop('_id')
                    myCartList.append(item)

        return {'success': True, 'data': myCartList}
    except:
        return {'success': False}


@cart.get('/{id}', dependencies=[Depends(jwtBearer())])
async def get_cart_item(id: str):
    cartItem = serializeList(db.cart.aggregate([
        {
            '$match': {
                '_id': ObjectId(id),
            }
        },
        {
            '$sort': {
                'created_at': -1
            }
        },
        {
            '$lookup': {
                'from': 'voucher',
                'localField': 'ticketId',
                'foreignField': '_id',
                'as': 'items'
            }
        }
    ]))

    currentCartItem = cartItem[0]['items'][0]
    currentCartItem['id'] = str(currentCartItem['_id'])
    currentCartItem.pop('_id')

    return currentCartItem


@cart.post('', dependencies=[Depends(jwtBearer())])
async def add_cart_item(ticketId: str, Authorization: str = Header(default=None)):
    try:
        userId = get_userId_from_request(Authorization)
        id = ObjectId()

        ticket = {
            '_id': id,
            'userId': userId,
            'ticketId': ObjectId(ticketId),
            'created_at': datetime.datetime.now(),
        }
        print(ticket)

        db.cart.insert_one(dict(ticket))
        cartItem = await get_cart_item(str(id))

        return {'success': True, 'message': 'add ticket successfully', 'data': cartItem}
    except:
        return {'success': False}


@cart.delete('/{id}')
async def delete_cart(id):
    return serializeDict(db.cart.find_one_and_delete({'_id': ObjectId(id)}))


@cart.post('/paypal/create-order', dependencies=[Depends(jwtBearer())])
async def createPaypalOrder(order: object = Body(default=None)):
    try:
        accessToken = await generate_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accessToken}",
        }

        async with httpx.AsyncClient(base_url=PAYPAL_BASE_URL, headers=headers) as client:
            response = await client.post("/v2/checkout/orders", json=order)

            return response.json()
    except:
        return {'success': False}


@cart.post('/paypal/approve-order', dependencies=[Depends(jwtBearer())])
async def createPaypalOrder(data: PaypalApprove):
    try:
        accessToken = await generate_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accessToken}",
        }

        async with httpx.AsyncClient(base_url=PAYPAL_BASE_URL, headers=headers) as client:
            response = await client.post(f"/v2/checkout/orders/{data.orderId}/capture")

            return response.json()
    except:
        return {'success': False}
