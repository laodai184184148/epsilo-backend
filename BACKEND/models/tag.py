
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer,primary_key=True, autoincrement=True)  
    sim_number = Column(String(45),primary_key=True)  
    title  = Column(String(200))  

