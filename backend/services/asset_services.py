from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from backend.db_models.assets import Transaction
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID

from backend.schemas.assets import CreateTransaction

import httpx
import yfinance as yf


async def get_holdings_from_symbol(db: AsyncSession, user_id:UUID, symbol:str):
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
    crypto_prices = await get_crypto_prices(crypto)
    stock_prices = await get_stock_prices(stocks)

    return crypto_prices | stock_prices

async def get_curr_holdings(db: AsyncSession, user_id: UUID):
    curr_holdings = {} # {api_id:{avg_price: float, quantity: float, type: str}}
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == user_id
        )
        .order_by(Transaction.created_at.asc())
    )

    transactions = result.scalars().all()

    for t in transactions:
        if str(t.action) == "BUY":
            transaction_api_id = str(t.api_id)
            if transaction_api_id in curr_holdings:
                curr_holdings[transaction_api_id]["avg_price"] = get_curr_holdings_helper(
                    curr_holdings[transaction_api_id]["avg_price"],
                    t.price_of_one,
                    curr_holdings[transaction_api_id]["quantity"],
                    t.quantity
                )
                curr_holdings[transaction_api_id]["quantity"] += t.quantity
            else:
                curr_holdings[transaction_api_id] = {}
                curr_holdings[transaction_api_id]["avg_price"] = t.price_of_one
                curr_holdings[transaction_api_id]["quantity"] = t.quantity
                curr_holdings[transaction_api_id]["type"] = t.asset_type

        else: # if the action is SELL
            transaction_api_id = str(t.api_id)
            if transaction_api_id in curr_holdings:
                curr_holdings[transaction_api_id]["quantity"] -= t.quantity

    return curr_holdings

def get_curr_holdings_helper(curr_avg: float, new_price: float, curr_quantity: float, new_quantity: float):
    total_cost = (curr_avg * curr_quantity) + (new_price * new_quantity)
    return total_cost / (curr_quantity + new_quantity)

async def get_usd_to_cad():
    url = "https://open.er-api.com/v6/latest/USD"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()

    cad = data.get("rates", {}).get("CAD")

    return float(cad)

async def get_crypto_prices(api_ids: list[str]):
    if not api_ids:
        return {}

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": ",".join(api_ids), # Required format for coingecko "bitcoin,ethereum,solana"
        "vs_currencies": "cad"
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        data = res.json() # convert to python dict

    prices = {} # api_id: price

    for api_id in api_ids:
        if api_id in data:
            if "cad" in data[api_id]:
                prices[api_id] = data[api_id]["cad"]
            else:
                prices[api_id] = 0.0
        else:
            prices[api_id] = 0.0

    print(prices)

    return prices

async def get_stock_prices(symbols: list[str]):
    if not symbols:
        return {}

    tickers = yf.Tickers(" ".join(symbols)) # format into "AAPL TSLA VCN"

    prices = {} # symbol: price
    conversion = await get_usd_to_cad()

    for symbol in symbols:
        try:
            ticker = tickers.tickers[symbol]
            usd_price = float(ticker.fast_info["last_price"]) # fetch most recent trading price
            prices[symbol] = usd_price * conversion
        except Exception: # invalid symbols just fail silently
            prices[symbol] = 0.0

    print(prices)

    return prices

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

async def current_quantity(db: AsyncSession, user_id:UUID, symbol:str) -> float:
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
                "asset_type": str(trans.asset_type),
                "symbol": str(trans.symbol),
                "api_ids": str(trans.api_id),
                "price_of_one": float(trans.price_of_one),
                "quantity": float(trans.quantity),
                "created_at": trans.created_at.isoformat()
            }
        )
    return transactions_data
