
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class  import Base

class Channel(Base):
    __tablename__ = "channel"
    id = Column(String(45), primary_key=True)
    name  = Column(String(45))  

