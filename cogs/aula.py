from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40))

Base.metadata.create_all(engine)
