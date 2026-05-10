import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi_users import BaseUserManager, UUIDIDMixin, models
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
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

    async def on_after_register(self,
                                user: User,
                                request: Request | None = None):
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        verify_url = f"http://localhost:5173/verify?token={token}"
        print(verify_url)


class Transaction(Base):
    __tablename__ = "transactions"
    # Note I assume every purchase will be done using CAD and user will convert before typing in pricing

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    action = Column(String, nullable=False) # Either BUY or SELL
    profit = Column(Numeric(20, 10), default=0)
    asset_type = Column(String, nullable=False) # type of purchase (stock, crypto, currency, etc.)
    symbol = Column(String, nullable=False) # symbol or purchase (BTC, SMP500, AAPL, USD, etc.)
    api_id = Column(String, nullable=False)
    price_of_one = Column(Numeric(20, 10), nullable=False)
    quantity = Column(Numeric(20, 10), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="transactions")
