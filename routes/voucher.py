from fastapi import APIRouter
from schemas.user import serializeDict, serializeList
from models.voucher import Voucher
from config.db import db
from bson import ObjectId

voucher = APIRouter()

@voucher.get('')
async def get_all_voucher():
  tickets = serializeList(db.voucher.find())
  return tickets

@voucher.get('/{id}')
async def get_voucher_detail(id):
  return serializeDict(db.voucher.find_one({'_id': ObjectId(id)}))

@voucher.post('')
async def add_voucher(voucher: Voucher):
  db.voucher.insert_one(dict(voucher))
  return {'success': True, 'data': voucher}

@voucher.put('/{id}')
async def update_voucher(id, voucher: Voucher):
  db.voucher.update_one({'_id': ObjectId(id)}, {
    '$set': dict(voucher),
  })
  return serializeDict(db.voucher.find_one({'_id': ObjectId(id)}))

@voucher.delete('/{id}')
async def delete_voucher(id):
  return serializeDict(db.voucher.find_one_and_delete({'_id': ObjectId(id)}))