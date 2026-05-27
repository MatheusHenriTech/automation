from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    username = Column(String)
    coins = Column(Integer, default=0)
    daily = Column(DateTime, default=None)