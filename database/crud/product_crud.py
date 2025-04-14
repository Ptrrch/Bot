from typing import Any, Coroutine

from sqlalchemy import and_, select

from database.engine import connection
from database.models import Product

@connection
async def create_product(session, data:dict) -> Product | None:
    product = await session.scalar(select(Product).where(and_(
        Product.owned_id == data['owned_id'],
        Product.title == data['title']
        )))
    if not product:
        new_product = Product(
            owned_id = data['owned_id'],
            title = data['title'],
            description = data['description'],
            price = data['price'],
            img = data['img']
        )
        session.add(new_product)
        await session.commit()
        return new_product
    


@connection
async def get_products(session, data:dict) -> list[Product] | None:
    products = await session.scalars(select(Product).where(Product.owned_id == data['owned_id']))
    if products:
        return products


@connection
async def get_one_product(session, data:dict) -> Product | None:
    product = await session.scalar(select(Product).where(Product.id == data['id']))
    if product:
        return product



@connection
async def update_product(session, data:dict) -> Product | None:
    product = await session.scalar(select(Product).where(Product.id == data['id']))
    if product:
        product.title = data['title']
        product.description = data['description']
        product.price = data['price']
        product.img = data['img']
        await session.commit()



@connection
async def delete_product(session, data:dict) -> list[Product] | None:
    product = await session.scalar(select(Product).where(Product.id == data['id']))
    if product:
        await session.delete(product)
        await session.commit()
   
