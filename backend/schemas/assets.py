from pydantic import BaseModel
from fastapi_users import schemas
import uuid

class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str

class UserCreate(schemas.BaseUserCreate):
    name: str

class UserUpdate(schemas.BaseUserUpdate):
    pass
