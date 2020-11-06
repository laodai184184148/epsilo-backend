
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer,primary_key=True, autoincrement=True)
    phone_owner = Column(String(45))
    time = Column(String(45))
    otp = Column(String(45))
    raw_message = Column(String(200))  
    from_number = Column(String(45))  
    date= Column(String(45)) 
    shop_id = Column(String(45))   
  

