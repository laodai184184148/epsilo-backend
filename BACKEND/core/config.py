
from pydantic import  BaseSettings
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

class Settings(BaseSettings):
#config
    BAUDRATE = 9600

    tries = 3
    
    SMS_SIGNAL = ["+CMTI: \"MT\"","+CMTI: \"SM\""]
    
    GSM_NAME = ["ttyACM","tty.usbmodem"]
    
    providers = {"45204":"viettel",
             "45201":"mobifone",
             "45202":"vinaphone",
             "45205":"vietnamobile",
             "i-tel":"vietnamobile",
             "45208":"vietnamobile"}
    
    ERRORS_CODE = ["ERROR","+CUSD: 4"]
#global variables
    list_Device = []
    
    repeat = True
    
    main_Thread = []
################################
    AUTH_PLUGIN:str ='mysql_native_password'

    MYSQL_SERVER :str =os.getenv("MYSQL_SERVER")

    MYSQL_PORT :int =os.getenv("MYSQL_PORT")

    MYSQL_PASSWORD :str =os.getenv("MYSQL_PASSWORD")

    MYSQL_USER:str =os.getenv("MYSQL_USER")

    MYSQL_DB:str =os.getenv("MYSQL_DB")
    
    PROJECT_NAME:str=os.getenv("PROJECT_NAME")
    SQLACHEMY_CONNECTION_STRING = 'mysql+pymysql://{}:{}@{}/{}'.format(MYSQL_USER,quote_plus(MYSQL_PASSWORD), MYSQL_SERVER, MYSQL_DB)
    
    SECRET_KEY:str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    
    ALGORITHM:str = "HS256"
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 1000

    class Config:
        case_sensitive = True
settings = Settings()

