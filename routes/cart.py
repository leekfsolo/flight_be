from fastapi import APIRouter, Header, Depends, Body
from schemas.user import serializeDict, serializeList
from config.db import db
from bson import ObjectId
from provider.authProvider import get_userId_from_request
from provider.jwtProvider import jwtBearer
import datetime

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
            'from': 'tickets', 
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
  
    db.cart.insert_one({
      '_id': id,
      'userId': userId,
      'ticketId': ObjectId(ticketId),
      'created_at': datetime.datetime.now(),
    })
    
    cartItem = await get_cart_item(str(id), Authorization)
    
    return {'success': True, 'message': 'add ticket successfully', 'data': cartItem}
  except:
    return {'success': False}

@cart.delete('/{id}')
async def delete_cart(id):
  return serializeDict(db.cart.find_one_and_delete({'_id': ObjectId(id)}))