
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey,Boolean,Float
from db.base_class import Base

class Sim(Base):
    __tablename__ = "sim"
    sim_number = Column(String(45),primary_key=True)  
    tty_gateway  = Column(String(45))    
    status = Column(Boolean)   
    expire_date=Column(String(45))
    balance =Column(Float(45))
    check=Column(String(45)) 

