import asyncio
from datetime import datetime, timedelta
from typing import Optional, Literal

from fastapi import HTTPException, Depends, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.authentication.authentication import current_active_user
from backend.db.database import get_async_session
from backend.db_models.assets import Transaction, User
from backend.schemas.assets import CreateTransaction, UpdateTransaction
from backend.services.asset_services import current_quantity, create_holding_filter, \
    turn_list_to_dict, calculate_profit_for_one_transaction, get_curr_holdings_prices, \
    get_holdings_at_time, get_portfolio_value_at, get_cash_flow_between, get_total_realized_profit

router = APIRouter()

@router.get("/transactions/{trans_id}")
async def return_transaction_with_id(
        trans_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    """
    When given an id return exactly what transaction it is, if the id is not found return a 404 error.

    Note that the user won't actually be entering a transaction id, this is mainly used as a helper to
    fetch certain transactions and also so when the user is on the transactions page, they can select a specific transaction
    and based on what they click the front end will automatically send the id here to return the information of
    the transaction.
    """
    result = await session.execute(
        select(Transaction).where(
            Transaction.user_id == current_user.id,
            Transaction.id == trans_id
        )
    )

    transaction = result.scalars().first() # we use .first since obviously when we are querying based off a transaction id there should only be one
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.delete("/transactions/{trans_id}")
async def delete_transaction_with_id(
        trans_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    """
    When given an id delete the transaction from our history.

    Note that the user won't actually be entering a transaction id, this is mainly used as a helper to
    fetch certain transactions and also so when the user is on the transactions page, they can select a specific transaction
    and based on what they click the front end will automatically send the id here to delete the transaction.
    """
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

@router.put("/transactions/{trans_id}")
async def update_transaction_with_id(
        trans_id: str,
        updates: UpdateTransaction,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    """
    When given an id delete the transaction from our history.

    Note that the user won't actually be entering a transaction id, this is mainly used as a helper to
    fetch certain transactions and also so when the user is on the transactions page, they can select a specific transaction
    and based on what they click the front end will automatically send the id here to delete the transaction.
    """
    transaction = return_transaction_with_id(trans_id, session, current_user)

    if updates.symbol:
        transaction.symbol = updates.symbol
    if updates.action:
        transaction.action = updates.action
    if updates.asset_type:
        transaction.asset_type = updates.asset_type
    if updates.price_of_one:
        transaction.price_of_one = updates.price_of_one
    if updates.quantity:
        transaction.quantity = updates.quantity
    if updates.api_id:
        transaction.api_id = updates.api_id

@router.get("/transactions")
async def return_holdings_with_filter(
        symbol: Optional[str] = Query(None),
        action: Optional[Literal["BUY", "SELL"]] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),

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
    profit_calculated = 0.0
    if data.action == "SELL":
        curr_holdings = await current_quantity(session, current_user.id, data.symbol)
        if data.quantity > curr_holdings:
            raise HTTPException(status_code=409, detail="Insufficient holdings") # Error if you are trying to sell more than you have
        profit_calculated = await calculate_profit_for_one_transaction(session,
                                                                 current_user.id,
                                                                 data)  # Calculate profit for the sell

    transaction = Transaction(
        action=data.action,
        profit=profit_calculated,
        asset_type=data.asset_type,
        symbol=data.symbol,
        api_id=data.api_id,
        price_of_one=data.price_of_one,
        quantity=data.quantity,
        user_id=current_user.id
    )
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction

@router.get("/holdings")
async def current_holdings(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    return await get_holdings_at_time(session, current_user.id, datetime.utcnow())

@router.get("/portfolio")
async def portfolio_stats(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    now = datetime.utcnow()

    # current
    holdings = await get_holdings_at_time(session, current_user.id, now)

    if not holdings:
        return {
            "value": 0.0,
            "profit": 0.0,
            "daily": 0.0,
            "weekly": 0.0,
            "monthly": 0.0,
            "yearly": 0.0
        }

    curr_prices = await get_curr_holdings_prices(holdings)

    total_value = 0.0
    unrealized_profit = 0.0

    for api_id, data in holdings.items():
        price = float(curr_prices.get(api_id, 0.0))
        quantity = float(data["quantity"])
        avg_price = float(data["avg_price"])

        position_value = price * quantity
        cost_basis = avg_price * quantity

        total_value += position_value
        unrealized_profit += (position_value - cost_basis)

    # ---- TIME WINDOWS ----
    one_day = now - timedelta(days=1)
    seven_days = now - timedelta(days=7)
    thirty_one_days = now - timedelta(days=31)
    three_sixty_five_days = now - timedelta(days=365)

    # ---- PARALLEL TASKS ----
    value_tasks = [
        get_portfolio_value_at(session, current_user.id, one_day),
        get_portfolio_value_at(session, current_user.id, seven_days),
        get_portfolio_value_at(session, current_user.id, thirty_one_days),
        get_portfolio_value_at(session, current_user.id, three_sixty_five_days),
    ]

    cash_tasks = [
        get_cash_flow_between(session, current_user.id, one_day, now),
        get_cash_flow_between(session, current_user.id, seven_days, now),
        get_cash_flow_between(session, current_user.id, thirty_one_days, now),
        get_cash_flow_between(session, current_user.id, three_sixty_five_days, now),
    ]

    realized_task = get_total_realized_profit(session, current_user.id)

    results = await asyncio.gather(
        *value_tasks,
        *cash_tasks,
        realized_task
    )

    # ---- UNPACK RESULTS ----
    value_1d, value_7d, value_31d, value_365d = results[0:4]
    cash_1d, cash_7d, cash_31d, cash_365d = results[4:8]
    realized_profit = results[8]

    # ---- FINAL PROFITS ----
    daily_profit = (total_value - value_1d) - cash_1d
    weekly_profit = (total_value - value_7d) - cash_7d
    monthly_profit = (total_value - value_31d) - cash_31d
    yearly_profit = (total_value - value_365d) - cash_365d

    total_profit = unrealized_profit + realized_profit

    return {
        "value": total_value,
        "alltime": total_profit,
        "daily": daily_profit,
        "weekly": weekly_profit,
        "monthly": monthly_profit,
        "yearly": yearly_profit
    }
