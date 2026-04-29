import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas, models
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric, Computed
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
from starlette.requests import Request

load_dotenv()

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    name = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="user")

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = os.getenv("SECRET")
    verification_token_secret = os.getenv("SECRET")

    async def on_after_register(self, user: models.UP, request: Request | None = None) -> None:
        # Pass for now but later will add a email verification system
        pass


class Transaction(Base):
    __tablename__ = "transactions"
    # Note I assume every purchase will be done using CAD and user will convert before typing in pricing

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    action = Column(String, nullable=False) # Either BUY or SELL
    profit = Column(Numeric(20, 10), default=0)
    asset_type = Column(String, nullable=False) # type of purchase (stock, crypto, currency, etc.)
    symbol = Column(String, nullable=False) # symbol or purchase (BTC, SMP500, AAPL, USD, etc.)
    price_of_one = Column(Numeric(20, 10), nullable=False)
    quantity = Column(Numeric(20, 10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
