from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.crud.product_crud import create_product
from database.engine import connection
from database.models import Order, OrderProductAssociation


@connection
async def create_order(session) -> Order | None:
    order = await session.scalar(
        select(Order)
        .options(selectinload(Order.products_details))
    )

    if order:
        new_order = Order(
        )
        session.add(new_order)
        await session.commit()
        return new_order, new_order.id


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)
async def get_orders_assoc(session: AsyncSession, id: int) -> Order:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        ).where(Order.id == id)
    )
    order = await session.scalar(stmt)
    return order

@connection
async def create_order_assoc(session):
    product = await create_product(
        {'id': 1, 'owned_id': 1, 'title': "title", 'description': "description", 'price': 100}
    )
    first_product = await create_product(
        {'id': 2, 'owned_id': 2, 'title': "title2", 'description': "description", 'price': 300}
    )
    second_product = await create_product(
        {'id': 3, 'owned_id': 2, 'title': "title3", 'description': "description", 'price': 250}
    ) 
    await create_order({'id': '1'})
    await create_order({'id': '2'})
    await create_order({'id': '3'})
    orders = await get_orders_with_products_assoc(session)  # Передаем сессию
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=2,
                product=product
            )
        )
    order = await get_orders_assoc(session, 2)
    order.products_details.append(
        OrderProductAssociation(
            count =1,
            product = first_product
        )
    )
    order.products_details.append(
        OrderProductAssociation(
            count=2,
            product=second_product
        )
    )
    await session.commit()
