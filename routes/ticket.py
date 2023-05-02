from fastapi import APIRouter
from schemas.user import serializeDict, serializeList
from models.ticket import Ticket
from config.db import db
from bson import ObjectId

ticket = APIRouter()

@ticket.get('/')
async def get_all_tickets():
  tickets = serializeList(db.tickets.find())
  return tickets[0:10]

@ticket.get('/{id}')
async def get_ticket_detail(id):
  return serializeDict(db.tickets.find_one({'_id': ObjectId(id)}))

@ticket.post('/')
async def add_ticket(ticket: Ticket):
  db.tickets.insert_one(dict(ticket))
  return {'success': True, 'data': ticket}

@ticket.put('/{id}')
async def update_ticket(id, ticket: Ticket):
  db.tickets.update_one({'_id': ObjectId(id)}, {
    '$set': dict(ticket),
  })
  return serializeDict(db.tickets.find_one({'_id': ObjectId(id)}))

@ticket.delete('/{id}')
async def delete_ticket(id):
  return serializeDict(db.tickets.find_one_and_delete({'_id': ObjectId(id)}))