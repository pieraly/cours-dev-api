from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Jerseys(Base):
    __tablename__ = "jersey"

    name = Column(String)
    jersey_id = Column(Integer, primary_key=True, index=True)
    price = Column(Numeric)
    tags = Column(String)
    availability = Column(Boolean, default=True)
    stock = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')


class Clients(Base):
    __tablename__="client"
    
    client_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  
    
    
class Orders(Base):
    __tablename__="order"
    
    id= Column(Integer, primary_key=True, nullable=False)
    client_id= Column(Integer, ForeignKey("client.client_id", ondelete="RESTRICT"), nullable=False) 
    jersey_id = Column(Integer, ForeignKey("jersey.jersey_id", ondelete="RESTRICT"), nullable=False) 
    order_date=Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")