from pydantic import Field
from models.CustomBaseModels import CustomBaseModel
from bson import ObjectId
import datetime

class CartItem(CustomBaseModel):
	userId: ObjectId = Field(default=None)
	ticketId: ObjectId = Field(default=None)
	created_at: datetime = Field(default=datetime.datetime.now())