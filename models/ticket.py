from models.CustomBaseModels import CustomBaseModel
from pydantic import Field
import datetime

class Ticket(CustomBaseModel):
  type: str = Field(default=None)
  classType: str = Field(default=None)
  fromLocation: str = Field(default=None)
  toLocation: str = Field(default=None)
  startDate: datetime.datetime = Field(default=datetime.datetime.now())
  endDate: datetime.datetime = Field(default=datetime.datetime.now())
  quantity: int = Field(default=0)
  wifi: bool = Field(default=False)
  entertainment: bool = Field(default=False)
  meals: int = Field(default=0)
  price: float = Field(default=0)
  airline: int = Field(default=0)
  