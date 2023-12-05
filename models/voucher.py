from pydantic import Field
from models.CustomBaseModels import CustomBaseModel
import datetime

class Voucher(CustomBaseModel):
    voucherID: int = Field(...)
    voucherCode: str = Field(...)
    expirationDate: datetime.datetime = Field(default=datetime.datetime.now())
    numberOfProduct: int = Field(default=0)
    status: str = Field(default=None)
    originalPrice: float = Field(default=0)
    salePrice: float = Field(default=0)
    category: str = Field(default=None)
    brand: str = Field(default=None)
    location: str = Field(default=None)
    description: str = Field(default=None)
    image: str = Field(default=None)
