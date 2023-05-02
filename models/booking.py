from pydantic import Field
from models.CustomBaseModels import CustomBaseModel

class Booking(CustomBaseModel):
  ticketId: str = Field(default=None)
  paymentMethod: int = Field(default=0)
  luggage: bool = Field(default=False)
  firstname: str = Field(default=None)
  lastname: str = Field(default=None)
  email: str = Field(default=None)
  phone: str = Field(default=None)
	