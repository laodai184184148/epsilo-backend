from typing import List, Optional

from pydantic import BaseModel

class ShopBase(BaseModel):
    name: str


class ShopCreate(ShopBase):
    id: str
    postal_code: str
    channel_id:str
    correspond_apicall:str

class Shop(ShopBase):
    id: str
    postal_code: Optional[str] = None
    channel_id:Optional[str] = None
    correspond_apicall:Optional[str] = None
    channel_name:Optional[str] = None
    country_name:Optional[str] = None
    number_of_sim:Optional[int] = None
    shop_master_id:Optional[int] = None


    class Config:
        orm_mode = True