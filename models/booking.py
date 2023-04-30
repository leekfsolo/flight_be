from pydantic import BaseModel

class Booking(BaseModel):
  name: str
  password: str
  email: str