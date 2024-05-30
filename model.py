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
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))