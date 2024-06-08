# model.py
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    api_name = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    city = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first = Column(String)
    last = Column(String)
    address = Column(String)
    email = Column(String)
    balance = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))