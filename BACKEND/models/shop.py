
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Shop(Base):
    __tablename__ = "shop"
    id = Column(String(45), primary_key=True)
    name = Column(String(45))  
    postal_code = Column(String(45))    
    channel_id = Column(String(45))  
    correspond_apicall = Column(String(200))   
    shop_master_id=Column(Integer)

