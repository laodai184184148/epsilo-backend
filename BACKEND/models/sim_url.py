from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Sim_Url(Base):
    __tablename__ = "sim_url" 
    sim_number = Column(String(45),primary_key=True)  
    url = Column(String(45),primary_key=True) 
