import enum
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
	
	created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
	updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
	__tablename__ = "users"
	

	
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
	name: Mapped[str] = mapped_column(String(30)) 
	lastname: Mapped[str]
	number: Mapped[str] = mapped_column(String(20), unique=True) 
	type: Mapped[str] = mapped_column(String(50))  


	__mapper_args__ = {
        'polymorphic_identity': 'user',
		'polymorphic_on': 'type',
		'with_polymorphic': '*',
    }

	

class Product(Base):
	__tablename__ = "products"
	
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	owned_id: Mapped[int] = mapped_column(ForeignKey('citchens.id'))
	name: Mapped[str] = mapped_column(String(30))
	description: Mapped[str] = mapped_column(Text)
	price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
	img: Mapped[str] = mapped_column(String(150))
	orders: Mapped[list["Order"]] = relationship(
		secondary="order_product_association", 
		back_populates="products",
		)


class Citchen(User):
	__tablename__  = "citchens"
	id: Mapped[int] = mapped_column(None, ForeignKey('users.id'), primary_key=True)
	title: Mapped[str] = mapped_column(String(30))
	description: Mapped[str] = mapped_column(Text)
	city: Mapped[int] = mapped_column(ForeignKey('cities.id'))

	__mapper_args__ = {
        'polymorphic_identity': 'citchen', 
    }



class Client(User):
	__tablename__ = "clients"
	# __mapper_args__ = {
    #     'polymorphic_identity': 'client',
    #     'inherit_condition': (id == User.id),  
    # }
	
	id: Mapped[int] = mapped_column(None, ForeignKey('users.id'), primary_key=True)
	adress: Mapped[str] = mapped_column(String(150))
	orders: Mapped[list["Order"]] = relationship("Order", back_populates="client", cascade="all, delete-orphan")
	state: Mapped[StateClient]

	__mapper_args__ = {
        'polymorphic_identity': 'client', 
    }


class Admin(User):
	__tablename__  = "admins"
	# __mapper_args__ = {
    #     'polymorphic_identity': 'admin',
    #     'inherit_condition': (id == User.id),  
    # }
	id: Mapped[int] = mapped_column(None, ForeignKey('users.id'), primary_key=True)

	__mapper_args__ = {
        'polymorphic_identity': 'admin', 
    }


class Courier(User):
	__tablename__  = "couirers"
	# __mapper_args__ = {
    #     'polymorphic_identity': 'couirer',
    #     'inherit_condition': (id == User.id),  
    # }
	id: Mapped[int] = mapped_column(None, ForeignKey('users.id'), primary_key=True)
	
	__mapper_args__ = {
        'polymorphic_identity': 'courier', 
    }




class Order(Base):
	__tablename__  = "orders"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	state_order: Mapped[StateOrder]
	products: Mapped[list["Product"]] = relationship(
		secondary="order_product_association", 
		back_populates="orders",
		)

class City(Base):
	__tablename__ = "cities"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	tittle: Mapped[str]


class OrderProductAssociation(Base):
	__tablename__ = "order_product_association"
	__table_args__ = (
		UniqueConstraint(
			"order_id",
			"product_id",
			name = "idx_unique_order_product"
		),
	)
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
	product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
	count: Mapped[int] = mapped_column(default=1, server_default="1")

