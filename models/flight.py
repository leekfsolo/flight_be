from pydantic import BaseModel

class Flight(BaseModel):
  name: str
  password: str
  email: str