import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean


Base = declarative_base()

class Jersey(Base):
    __tablename__ = "jersey"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    tags = Column(String)
    availability = Column(Boolean, default=True)
    stock = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)
