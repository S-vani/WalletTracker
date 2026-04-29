from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from backend.db_models.assets import Transaction
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID

async def get_holdings_from_symbol(db: AsyncSession, user_id:UUID, symbol:str):
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.symbol == symbol
        )
    )

    return result.scalars().all()

def create_holding_filter(
                                user_id: UUID,
                                symbol: str | None = None,
                                action: str | None = None,
                                start_date: datetime | None = None,
                                end_date: datetime | None = None
                                ):
    query = select(Transaction).where(Transaction.user_id == user_id)

    if symbol:
        query = query.where(Transaction.symbol == symbol)

    if action:
        query = query.where(Transaction.action == action)

    if start_date:
        query = query.where(Transaction.created_at >= start_date)

    if end_date:  # Will always be true
        query = query.where(Transaction.created_at <= end_date)
    else:
        query = query.where(Transaction.created_at <= datetime.utcnow())

    return query

async def current_quantity(db: AsyncSession, user_id:UUID, symbol:str) -> float:
    lst = await get_holdings_from_symbol(db, user_id, symbol)
    selling = 0
    buying = 0
    for trans in lst:
        if trans.action == "SELL":
            selling += trans.quantity
        else:
            buying += trans.quantity

    return buying - selling

def turn_list_to_dict(lst):
    transactions_data = []
    for trans in lst:
        transactions_data.append(
            {
                "id": str(trans.id),
                "user_id": str(trans.user_id),
                "action": str(trans.action),
                "asset_type": str(trans.asset_type),
                "symbol": str(trans.symbol),
                "price_of_one": float(trans.price_of_one),
                "quantity": float(trans.quantity),
                "created_at": trans.created_at.isoformat()
            }
        )
    return transactions_data
