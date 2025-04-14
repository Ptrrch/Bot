import enum
from enum import StrEnum
import pytz
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ARRAY, BigInteger, DateTime, Float, ForeignKey, Integer, Text, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class StateClient(str, enum.Enum):
    positive = "Высокий рейтинг"
    default = "Обычный"
    negative = "Низкий рейтинг"
    blackList = "Черный список"


class UserForm(StrEnum):
    agree = "Согласен"
    disagree = "Несогласен"


class StateOrder(str, enum.Enum):
    request = "Заявка"
    inTheReview = "В рассмотрении"
    prepared = "Готовится"
    courierInform = "Собщили курьеру"
    inTheWay = "В пути"
    delivered = "Доставлен"
    cancelled = "Отменен"


class PaymentType(StrEnum):
    inCash = "Наличными"
    byCard = "Картой"


def get_default_time():
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz)
    return current_time


class Base(DeclarativeBase):
    __abstract__ = True


    created: Mapped[DateTime] = mapped_column(DateTime, default=get_default_time, server_default=func.now(), nullable=True)
    updated: Mapped[DateTime] = mapped_column(DateTime, default=get_default_time, server_default=func.now(), onupdate=get_default_time, nullable=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    state: Mapped[StateClient] = mapped_column(default=StateClient.default, server_default=StateClient.default)
    form: Mapped[UserForm] = mapped_column(default=UserForm.disagree, server_default=UserForm.disagree)


class Kitchen(Base):
    __tablename__ = "kitchens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, default="-", server_default="-")
    title: Mapped[str] = mapped_column(String(30), nullable=True, default="-", server_default="-")
    description: Mapped[str] = mapped_column(Text, nullable=True, default="-", server_default="-")
    number: Mapped[str] = mapped_column(String(20), nullable=True, default="-", server_default="-")
    address: Mapped[str] = mapped_column(String(30), nullable=True, default="-", server_default="-")
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=True)
    cities: Mapped["City"] = relationship(back_populates='kitchens')


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))

    kitchens: Mapped[list["Kitchen"]] = relationship(back_populates="cities")
    couriers: Mapped[list["Courier"]] = relationship(back_populates="cities")
    clients: Mapped[list["Client"]] = relationship(back_populates="cities")



class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    patronymic: Mapped[str] = mapped_column(String(30), nullable=True)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client", cascade="all, delete-orphan")
    state: Mapped[StateClient] = mapped_column(default=StateClient.default)
    number: Mapped[str|None] = mapped_column(String(20), unique=True)

    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=True)
    cities: Mapped["City"] = relationship("City", back_populates='clients')



class Admin(Base):
    __tablename__  = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str]
    number: Mapped[str|None] = mapped_column(String(20), unique=True)
 

class Courier(Base):
    __tablename__  = "couriers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True, default="-", server_default="-")
    lastname: Mapped[str] = mapped_column(String(20), nullable=True, default="-", server_default="-" )
    number: Mapped[str|None] = mapped_column(String(20), nullable=True, default="-", server_default="-")
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True, default="-", server_default="-")
    cities: Mapped["City"] = relationship( "City", back_populates="couriers")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="courier", cascade="all, delete-orphan")
    order_counter: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=True)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owned_id: Mapped[int|None] = mapped_column(ForeignKey('kitchens.id'))
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    img: Mapped[str] = mapped_column(String(150))
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )


class Order(Base):
    __tablename__  = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    state_order: Mapped[StateOrder] = mapped_column(default=StateOrder.request)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=True)
    client: Mapped["Client"] = relationship("Client", back_populates="orders")
    courier_id: Mapped[int] = mapped_column(ForeignKey("couriers.id"), nullable=True)
    courier: Mapped["Courier"] = relationship("Courier", back_populates="orders")
    delivery_time: Mapped[str] = mapped_column(String(30), default="Ближайшее", server_default="Ближайшее")
    address: Mapped[str] = mapped_column(String(40), default="-", server_default="-")
    payment_type: Mapped[PaymentType] = mapped_column(nullable=True)
    change_amount: Mapped[int] = mapped_column(nullable=True)
    order_price: Mapped[int] = mapped_column(Integer, nullable=True, default=0, server_default="0")
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name = "idx_unique_kitchen_city"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    count: Mapped[int] = mapped_column(default=1, server_default="1")

    order: Mapped["Order"] = relationship(
        back_populates="products_details"
    )
    product: Mapped["Product"] = relationship(
        back_populates="orders_details"
    )
