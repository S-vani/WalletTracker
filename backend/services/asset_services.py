from sqlalchemy.ext.asyncio import AsyncSession
from backend.db_models.assets import Transaction
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID

async def get_holdings(db: AsyncSession, user_id:UUID, symbol:str):
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.symbol == symbol
        )
    )

    return result.scalars().all()

async def current_quantity(db: AsyncSession, user_id:UUID, symbol:str) -> float:
    lst = await get_holdings(db, user_id, symbol)
    selling = 0
    buying = 0
    for trans in lst:
        if trans.action == "SELL":
            selling += trans.quantity
        else:
            buying += trans.quantity

    return buying - selling
