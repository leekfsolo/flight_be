from pydantic import Field
from models.CustomBaseModels import CustomBaseModel
from bson import ObjectId
import datetime

class CartItem(CustomBaseModel):
	created_at: datetime.datetime = Field(default=datetime.datetime.now())
	