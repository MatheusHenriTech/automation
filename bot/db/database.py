from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///database.db")

Session = sessionmaker(engine)
Base = declarative_base()