from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from backend.db_models.assets import Transaction
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID

from backend.schemas.assets import CreateTransaction


async def get_holdings_from_symbol(db: AsyncSession, user_id:UUID, symbol:str):
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.symbol == symbol
        )
    )

    return result.scalars().all()

async def calculate_profit_for_one_transaction(db: AsyncSession, user_id:UUID, data: CreateTransaction):
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.symbol == data.symbol
        )
        .order_by(Transaction.created_at.asc())
    )

    transactions = result.scalars().all()

    quantity = 0.0
    avg_cost = 0.0

    for t in transactions:
        if t.action == "BUY":
            qty = float(t.quantity)
            price = float(t.price_of_one)

            new_qty = quantity + qty

            avg_cost = (
                (quantity * avg_cost + qty * price) / new_qty
                if new_qty > 0 else 0.0
            )

            quantity = new_qty

        elif t.action == "SELL":
            qty = float(t.quantity)
            quantity -= qty

    sell_qty = float(data.quantity)
    sell_price = float(data.price_of_one)

    profit = (sell_price - avg_cost) * sell_qty

    return profit


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
