from pydantic import BaseModel
from fastapi_users import schemas
import uuid
from typing import Literal

class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str

class UserCreate(schemas.BaseUserCreate):
    name: str

class UserUpdate(schemas.BaseUserUpdate):
    pass

class CreateTransaction(BaseModel):
    symbol: str
    action: Literal["BUY", "SELL"]
    asset_type: str
    price_of_one: float
    quantity: float
