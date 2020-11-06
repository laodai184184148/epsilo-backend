from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Url(Base):
    __tablename__ = "url" 
    id = Column(Integer,primary_key=True, autoincrement=True)  
    url = Column(String(200)) 
