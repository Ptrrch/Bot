from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.crud.product_crud import create_product
from database.engine import connection
from database.models import Order, OrderProductAssociation, Product, StateOrder, PaymentType


@connection
async def create_order(session, address: str, payment_type: PaymentType, change_amount: int, client_id: int, delivery_time: str) -> int:
    order = Order(
        address = address,
        payment_type = payment_type,
        change_amount = change_amount,
        client_id = client_id,
        delivery_time = delivery_time
    )
    session.add(order)
    await session.commit()
    return order.id


@connection
async def change_order_address(session, address: str,order_id: int) -> int:
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.address = address
    await session.commit()

@connection
async def change_order_delivery_time(session, delivery_time: str,order_id: int) -> int:
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.delivery_time = delivery_time
    await session.commit()


@connection
async def change_order_price(session, order_id:int, price: int) -> int:
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.order_price = price
    await session.commit()


@connection
async def append_courier_for_order(session, order_id: int, courier_id: int):
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.courier_id = courier_id
    await session.commit()


@connection
async def change_order_change_amount(session, change_amount: int,order_id: int) -> int:
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.change_amount = change_amount
    await session.commit()


@connection
async def change_order_payment_type(session, payment_type: PaymentType,order_id: int) -> int:
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        if payment_type == PaymentType.byCard:
            order.payment_type = payment_type
            order.change_amount = 0
        else:
            order.payment_type = payment_type
    await session.commit()



@connection
async def delete_order_product_assoc(session, order_id:int):
    orders = await session.scalars(select(OrderProductAssociation).where(OrderProductAssociation.order_id == order_id))
    if orders:
        for item in orders:
            await session.delete(item)
        await session.commit()


@connection
async def change_state_order(session, order_id: int, order_state: StateOrder):
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.state_order = order_state
        await session.commit()

@connection
async def get_order(session, order_id:int):
    order = await session.scalar(select(Order).where(Order.id == order_id))
    if order:
        return order

@connection
async def get_orders(session, user_id:int):
    orders = await session.scalars(select(Order).where(Order.client_id == user_id))
    if orders:
        return orders




async def get_order_assoc(session: AsyncSession, id: int) -> Order:
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


async def get_orders_assoc(session: AsyncSession, client_id: int) -> Order:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        ).where(Order.client_id == client_id)
    )
    orders = await session.scalars(stmt)
    return orders


async def create_order_assoc(session: AsyncSession, order_id: int, product: Product, cnt: int):
    order = await get_order_assoc(session, order_id)
    order.products_details.append(
        OrderProductAssociation(
            count = cnt,
            product = product
        )
    )
    await session.commit()
