from typing import Optional
from pydantic import BaseModel



class SMSRequest(BaseModel):
    to_number: str
    message: str
    data:dict

class CallRequest(BaseModel):
    reciever_number :str
    data:dict

class EmailRequest(BaseModel):
    email:str
    subject:str
    message:str
    data: dict

class WhatsAppRequest(BaseModel):
    message:str
    phone_number:str
    data: dict