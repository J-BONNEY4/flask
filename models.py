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
       user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
       product_name:Mapped[str]=mapped_column(String(100))
       buying_price:Mapped[float]=mapped_column(Float)
       selling_price:Mapped[float]=mapped_column(Float)

class Purchase(Base):
       __tablename__="purchases"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("products.id"))
       # supplier_id:Mapped[int]=mapped_column(Integer)
       quantity:Mapped[int]=mapped_column(Integer)
       paid_amount:Mapped[float]=mapped_column(Float)
       created_at:Mapped[DateTime]=mapped_column(DateTime)

class Sale(Base):
       __tablename__="sales"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("products.id"))
       created_at:Mapped[DateTime]=mapped_column(DateTime)

class Sale_detail(Base):
       __tablename__="sale_details"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("products.id"))
       sale_id:Mapped[int]=mapped_column(Integer,ForeignKey("sales.id"))
       quantity:Mapped[int]=mapped_column(Integer)

# class Supplier(Base):
#        __tablename__="suppliers"
#        id:Mapped[int]=mapped_column(Integer,primary_key=True)
#        product_id:Mapped[str]=mapped_column(String,ForeignKey("products.id"))
#        Supplier_name:Mapped[str]=mapped_column(String(100))
#        phone:Mapped[str] = mapped_column(String(30))
#        email:Mapped[str]=mapped_column(String(100))
#        address:Mapped[str]=mapped_column(String)
#        country:Mapped[str]=mapped_column(String)

# class Stock(Base):
#        __tablename__="stock"
#        id:Mapped[str]=mapped_column(String,primary_key=True)
#        product_id:Mapped[str]=mapped_column(String,ForeignKey("products.id"))
#        supplier_name:Mapped[str]=mapped_column(String(100),ForeignKey("suppliers.id"))
#        stock_quantity:Mapped[str]=mapped_column(String)

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    amount: Mapped[float] = mapped_column(Float)
    method: Mapped[str] = mapped_column(String(70))
    trans_code:Mapped[str]=mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[DateTime] = mapped_column(DateTime)

