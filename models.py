from sqlalchemy import ForeignKey
from sqlalchemy import String,Integer,Float,DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
       pass

class User(Base):
       __tablename__="users"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       full_name:Mapped[str]=mapped_column(String(100))
       email:Mapped[str]=mapped_column(String(100))
       password:Mapped[str]=mapped_column(String(200))

class Product(Base):
       __tablename__="products"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       user_id:Mapped[int]=mapped_column(ForeignKey("user_id"))
       buying_price:Mapped[float]=mapped_column(Float)
       selling_price:Mapped[float]=mapped_column(Float)


class Purchase(Base):
       __tablename__="purchases"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("product_id"))
       supplier_id:Mapped[int]=mapped_column(Integer)
       quantity:Mapped[int]=mapped_column(Integer)
       buying_price:Mapped[float]=mapped_column(Float)
       total_amount:Mapped[float]=mapped_column(Float)
       purchase_date:Mapped[DateTime]=mapped_column(DateTime)

class Sale(Base):
       __tablename__="sales"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("product_id"))
       quantity:Mapped[int]=mapped_column(Integer)
       selling_date:Mapped[float]=mapped_column(Float)
       total_amount:Mapped[float]=mapped_column(Float)
       sale_date:Mapped[DateTime]=mapped_column(DateTime)


class Sales_details(Base):
       __tablename__="sale_details"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("product_id"))
       sale_id:Mapped[int]=mapped_column(Integer,ForeignKey("sale_id"))
       quantity:Mapped[int]=mapped_column(Integer)
       selling_date:Mapped[float]=mapped_column(Float)
       total_amount:Mapped[float]=mapped_column(Float)

class order(Base):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customer.id"))
    product_id: Mapped[str] = mapped_column(String, ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    order_status: Mapped[str] = mapped_column(String)
    order_date: Mapped[DateTime] = mapped_column(DateTime)
    total_amount: Mapped[float] = mapped_column(Float)

    
class Supplier(Base):
       __tablename__="suppliers"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[str]=mapped_column(String,ForeignKey("product_id"))
       Supplier_name:Mapped[str]=mapped_column(String(100))
       phone:Mapped[str] = mapped_column(String(30))
       email:Mapped[str]=mapped_column(String(100))
       address:Mapped[str]=mapped_column(String)
       country:Mapped[str]=mapped_column(String)

class stock(Base):
       __tablename__="stock"
       id:Mapped[str]=mapped_column(String,primary_key=True)
       product_id:Mapped[str]=mapped_column(String,ForeignKey("product_id"))
       supplier_name:Mapped[str]=mapped_column(String(100),ForeignKey("supplier_name"))
       stock_quantity:Mapped[str]=mapped_column(String)

class payment(Base):
    __tablename__ = "payment"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    order_id: Mapped[str] = mapped_column(String, ForeignKey("order.id"))
    amount: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str] = mapped_column(String(70))
    payment_status: Mapped[str] = mapped_column(String(30))
    payment_date: Mapped[DateTime] = mapped_column(DateTime)