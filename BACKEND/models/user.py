
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from db.base_class import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True, autoincrement=True)  
    user_name  = Column(String(45))  
    first_name = Column(String(45))  
    last_name = Column(String(45))    
    role = Column(String(45)) 
    last_login = Column(DateTime)  
    activate = Column(Boolean)

