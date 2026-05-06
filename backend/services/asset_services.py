from datetime import datetime, timedelta

import httpx
import yfinance as yf
from sqlalchemy import select, func, case
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db_models.assets import Transaction
from backend.schemas.assets import CreateTransaction


async def get_holdings_from_symbol(db: AsyncSession, user_id: UUID, symbol: str):
    """
    Return a dictionary that maps many things including the total value of the portfolio, the daily, weekly, monthly, yearly
    and all time profits.
    """
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.symbol == symbol
        )
    )

    return result.scalars().all()


async def get_curr_holdings_prices(holdings: dict[str, dict[str, float | str]]):
    crypto = []
    stocks = []

    for ids in holdings:
        if str(holdings[ids]["type"]) == "crypto":
            crypto.append(str(ids))
        elif str(holdings[ids]["type"]) == "stock":
            stocks.append(str(ids))

    # The 2 variables below are dicts like {api_id: curr_price}
    crypto_prices = await get_crypto_prices_at(crypto, datetime.utcnow())
    stock_prices = await get_stock_prices_at(stocks, datetime.utcnow())

    return crypto_prices | stock_prices


async def get_total_realized_profit(db: AsyncSession, user_id: UUID):
    result = await db.execute(
        select(func.coalesce(func.sum(Transaction.profit), 0.0))
        .where(
            Transaction.user_id == user_id,
            Transaction.action == "SELL"
        )
    )

    return float(result.scalar_one())


async def get_cash_flow_between(
        db: AsyncSession,
        user_id: UUID,
        start: datetime,
        end: datetime
):
    result = await db.execute(
        select(
            func.coalesce(  # if there's no rows with these props return 0.0 instead of null
                func.sum(
                    (Transaction.price_of_one * Transaction.quantity) *
                    case(
                        (Transaction.action == "BUY", 1),
                        else_=-1
                    )
                ),
                0.0
            )
        ).where(
            Transaction.user_id == user_id,
            Transaction.created_at > start,
            Transaction.created_at <= end
        )
    )

    return float(result.scalar_one())


async def get_portfolio_value_at(
        db: AsyncSession,
        user_id: UUID,
        timestamp: datetime
):
    holdings = await get_holdings_at_time(db, user_id, timestamp)

    if not holdings:
        return 0.0

    crypto = []
    stocks = []

    for api_id, data in holdings.items():
        if data["type"] == "crypto":
            crypto.append(api_id)
        else:
            stocks.append(api_id)

    crypto_prices = await get_crypto_prices_at(crypto, timestamp)
    stock_prices = await get_stock_prices_at(stocks, timestamp)

    prices = crypto_prices | stock_prices

    total_value = 0.0

    for api_id, data in holdings.items():
        price = float(prices.get(api_id, 0.0))
        quantity = float(data["quantity"])
        total_value += price * quantity

    return total_value


async def get_holdings_at_time(
        db: AsyncSession,
        user_id: UUID,
        timestamp: datetime
):
    curr_holdings = {}

    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.user_id == user_id,
            Transaction.created_at <= timestamp
        )
        .order_by(Transaction.created_at.asc())
    )

    transactions = result.scalars().all()

    for t in transactions:
        api_id = str(t.api_id)

        if str(t.action) == "BUY":
            if api_id in curr_holdings:
                curr_holdings[api_id]["avg_price"] = get_holdings_helper(
                    curr_holdings[api_id]["avg_price"],
                    t.price_of_one,
                    curr_holdings[api_id]["quantity"],
                    t.quantity
                )
                curr_holdings[api_id]["quantity"] += t.quantity
            else:
                curr_holdings[api_id] = {
                    "avg_price": t.price_of_one,
                    "quantity": t.quantity,
                    "type": t.asset_type
                }

        else:  # SELL
            if api_id in curr_holdings:
                curr_holdings[api_id]["quantity"] -= t.quantity

    return curr_holdings


async def get_holdings_at_time_list(
        db: AsyncSession,
        user_id: UUID,
        timestamp: datetime
):
    result = await get_holdings_at_time(db, user_id, timestamp)
    curr_holdings_list = []

    for key, value in result.items():
        curr_holdings_list.append(
            {"symbol": key, "avg_price": value["avg_price"], "quantity": value["quantity"], "type": value["type"]})

    return curr_holdings_list


def get_holdings_helper(curr_avg: float, new_price: float, curr_quantity: float, new_quantity: float):
    total_cost = (curr_avg * curr_quantity) + (new_price * new_quantity)
    return total_cost / (curr_quantity + new_quantity)


async def get_usd_to_cad():
    url = "https://open.er-api.com/v6/latest/USD"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()

    cad = data.get("rates", {}).get("CAD")

    return float(cad)


async def get_crypto_prices_at(api_ids: list[str], timestamp: datetime):
    if not api_ids:
        return {}

    prices = {}

    ts = int(timestamp.timestamp())

    async with httpx.AsyncClient(timeout=10) as client:
        for api_id in api_ids:
            url = "https://min-api.cryptocompare.com/data/v2/histoday"

            params = {
                "fsym": api_id.upper(),
                "tsym": "CAD",
                "limit": 1,
                "toTs": ts
            }

            res = await client.get(url, params=params)

            data = res.json()

            # last available daily close
            close_price = data["Data"]["Data"][0]["close"]

            prices[api_id] = float(close_price)

    return prices


async def get_stock_prices_at(symbols: list[str], timestamp: datetime):
    if not symbols:
        return {}

    tickers = yf.Tickers(" ".join(symbols))
    conversion = await get_usd_to_cad()

    prices = {}

    for symbol in symbols:
        ticker = tickers.tickers[symbol]

        hist = ticker.history(
            start=timestamp.date(),
            end=timestamp.date() + timedelta(days=1),
            interval="1d"
        )

        if not hist.empty:
            close_price = float(hist["Close"].iloc[0])
            prices[symbol] = close_price * conversion
        else:
            prices[symbol] = 0.0

    return prices


async def calculate_profit_for_one_transaction(db: AsyncSession, user_id: UUID, data: CreateTransaction):
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
        if str(t.action) == "BUY":
            qty = float(t.quantity)
            price = float(t.price_of_one)

            new_qty = quantity + qty

            avg_cost = (
                (quantity * avg_cost + qty * price) / new_qty
                if new_qty > 0 else 0.0
            )

            quantity = new_qty

        elif str(t.action) == "SELL":
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


async def current_quantity(db: AsyncSession, user_id: UUID, symbol: str) -> float:
    lst = await get_holdings_from_symbol(db, user_id, symbol)
    selling = 0
    buying = 0
    for trans in lst:
        if str(trans.action) == "SELL":
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
                "profit": float(trans.profit),
                "asset_type": str(trans.asset_type),
                "symbol": str(trans.symbol),
                "api_ids": str(trans.api_id),
                "price_of_one": float(trans.price_of_one),
                "quantity": float(trans.quantity),
                "created_at": trans.created_at.isoformat()
            }
        )
    return transactions_data
