from typing import Any, Coroutine

from sqlalchemy import select

from database.engine import connection
from database.models import Product

@connection
async def create_product(session, data:dict) -> Product | None:
    product = await session.scalar(select(Product).where(Product.id == data['id']))
    if not product:
        new_product = Product(
            owned_id = data['owned_id'],
            title = data['title'],
            description = data['description'],
            price = data['price']
        )
        session.add(new_product)
        await session.commit()
        return new_product