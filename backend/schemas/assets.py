from pydantic import BaseModel
from fastapi_users import schemas
import uuid
from typing import Literal, Optional

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
    api_id: str

class UpdateTransaction(BaseModel):
    symbol: Optional[str]
    action: Optional[Literal["BUY", "SELL"]]
    asset_type: Optional[str]
    price_of_one: Optional[float]
    quantity: Optional[float]
    api_id: Optional[str]
