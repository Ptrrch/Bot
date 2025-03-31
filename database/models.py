import enum
from enum import StrEnum
from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ARRAY, BigInteger, DateTime, Float, ForeignKey, Integer, Text, String, UniqueConstraint, func, \
    Boolean
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
    paidFor = "Оплачен"
    prepared = "Готовится"
    ready = "Готово"
    inTheWay = "В пути"
    delivered = "Доставлен"
    cancelled = "Отменен"


class Base(DeclarativeBase):

    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), server_default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    state: Mapped[StateClient] = mapped_column(default=StateClient.default, server_default=StateClient.default)
    form: Mapped[UserForm] = mapped_column(default=UserForm.disagree, server_default=UserForm.disagree)


class Kitchen(Base):
    __tablename__ = "kitchens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    number: Mapped[str] = mapped_column(String(20), unique=True)
    address: Mapped[str] = mapped_column(String(30))
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'), nullable=True)
    cities: Mapped["City"] = relationship(back_populates='kitchens')


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))

    kitchens: Mapped[list["Kitchen"]] = relationship(back_populates="cities")
    couriers: Mapped[list["Courier"]] = relationship(back_populates="cities")



class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client", cascade="all, delete-orphan")
    state: Mapped[StateClient] = mapped_column(default=StateClient.default)
    number: Mapped[str|None] = mapped_column(String(20), unique=True)



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
    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str]
    number: Mapped[str|None] = mapped_column(String(20), unique=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True)
    cities: Mapped["City"] = relationship( "City", back_populates="couriers")


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
    state_order: Mapped[StateOrder] = mapped_column(default=StateOrder.inTheReview)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=True)
    client: Mapped["Client"] = relationship("Client", back_populates="orders")
    delivery_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    demo: Mapped[bool] = mapped_column(Boolean, default=False, server_default="False")
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
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
