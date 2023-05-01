from fastapi import APIRouter
from schemas.user import serializeDict,serializeList
from models.user import UserLogin,User
from config.db import db
from bson import ObjectId
from provider.authProvider import get_password_hash

user = APIRouter()

@user.get('/')
async def get_all_users():
  return serializeList(db.user.find())

@user.get('/{id}')
async def get_user(id):
  return serializeDict(db.user.find_one({'_id': ObjectId(id)}))

@user.post('/')
async def add_user(user: UserLogin):
  userDB = {
    'email': user.email,
    'hashed_password': get_password_hash(user.password),
  }
  db.user.insert_one(userDB)
  return serializeList(db.user.find())

@user.put('/{id}')
async def update_user(id, user: UserLogin):
  db.user.update_one({'_id': ObjectId(id)}, {
    '$set': dict(user),
  })
  return serializeDict(db.user.find_one({'_id': ObjectId(id)}))

@user.delete('/{id}')
async def delete_user(id):
  return serializeDict(db.user.find_one_and_delete({'_id': ObjectId(id)}))