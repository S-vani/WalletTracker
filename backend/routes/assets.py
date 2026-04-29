import uuid
from datetime import datetime
from tkinter.tix import Select

from fastapi import HTTPException, File, UploadFile, Form, Depends, APIRouter
from sqlalchemy import select, Numeric
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Literal, Optional

from backend.authentication.authentication import current_active_user
from backend.db.database import get_async_session
from backend.db_models.assets import Transaction, User
from backend.schemas.assets import CreateTransaction

from backend.services.asset_services import get_holdings_from_symbol, current_quantity, create_holding_filter, \
    turn_list_to_dict

router = APIRouter()

@router.get("/transactions/{trans_id}")
async def return_holdings_with_id(
        trans_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Transaction).where(
            Transaction.user_id == current_user.id,
            Transaction.id == trans_id
        )
    )

    transaction = result.scalars().first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.delete("/transactions/{trans_id}")
async def delete_holding_with_id(
        trans_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    holding = await session.execute(
        select(Transaction).where(
            Transaction.user_id == current_user.id,
            Transaction.id == trans_id
        )
    )
    result = holding.scalars().first()

    if result is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    await session.delete(result)
    await session.commit()

    return result


@router.get("/transactions")
async def return_holdings_with_filter(
        symbol: str | None = None,
        action: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    query = create_holding_filter(current_user.id, symbol, action, start_date, end_date)

    result = await session.execute(query.order_by(Transaction.created_at.desc()))
    result = result.scalars().all()

    return turn_list_to_dict(result)

@router.post("/transactions")
async def make_transaction(
        data: CreateTransaction,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if data.action == "SELL":
        curr_holdings = await current_quantity(session, current_user.id, data.symbol)
        if data.quantity > curr_holdings:
            raise HTTPException(status_code=409, detail="Insufficient holdings") # Error if you are trying to sell more than you have

    transaction = Transaction(
        action=data.action,
        asset_type=data.asset_type,
        symbol=data.symbol,
        price_of_one=data.price_of_one,
        quantity=data.quantity,
        user_id=current_user.id
    )
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction
