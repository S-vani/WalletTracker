import uuid

from fastapi import HTTPException, File, UploadFile, Form, Depends, APIRouter
from sqlalchemy import select, Numeric
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Literal

from backend.authentication.authentication import current_active_user
from backend.db.database import get_async_session
from backend.db_models.assets import Transaction, User
from backend.schemas.assets import CreateTransaction

from backend.services.asset_services import get_holdings, current_quantity

router = APIRouter()

@router.get("/holdings/{symbol}")
async def return_holdings(
        symbol: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user),
):
    return await get_holdings(session, current_user.id, symbol)

@router.post("/transaction")
async def make_transaction(
        data: CreateTransaction,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if data.action == "SELL":
        curr_holdings = await current_quantity(session, current_user.id, data.symbol)
        if data.quantity > curr_holdings:
            raise HTTPException(status_code=409, detail="Insufficient holdings") # Error if you are trying to sell more than you have

    purchase = Transaction(
        action=data.action,
        asset_type=data.asset_type,
        symbol=data.symbol,
        price_of_one=data.price_of_one,
        quantity=data.quantity,
        user_id=current_user.id
    )
    session.add(purchase)
    await session.commit()
    await session.refresh(purchase)
    return purchase

@router.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data =[]
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )

    return {"posts": posts_data}

@router.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
