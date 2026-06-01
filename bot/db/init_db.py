from db.database import Base, engine
from db import models  

def init_db():
    Base.metadata.create_all(bind=engine)