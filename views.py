from fastapi import APIRouter, UploadFile, File, Depends, Form
from typing import List, Optional
from services import sms_service,call_service,email_service,whatsapp_service
from schemas import SMSRequest,CallRequest,EmailRequest,WhatsAppRequest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from config.database import engine
from loguru import logger

router = APIRouter(prefix="/connect", tags=["Communication"])



async def save_to_db(data: dict):
    columns = ", ".join(data.keys())
    values = ", ".join(f":{key}" for key in data.keys())

    sql = text(f"""
        INSERT INTO communications_document ({columns})
        VALUES ({values})
        RETURNING id;
    """)

    try:
        with engine.begin() as conn:
            result = conn.execute(sql, data)
            inserted_id = result.scalar()  # Fetch the inserted ID
        return inserted_id
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return None  # Return None to indicate failure
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


@router.post("/send_sms")
async def send_sms_api(request: SMSRequest)  -> dict:
    response = await sms_service.send_sms(request.to_number, request.message)
    if response["status_code"]==200:
        data=request.data
        data["communication_medium"] = "SMS"
        data["phone_no"] = request.to_number
        data["text_content"] = request.message
        await save_to_db(request.data)
    return response


@router.post("/make_call")
async def make_call_api(request: CallRequest):
    response =  await call_service.initiate_call (request.reciever_number)
    if response["status_code"]==200:
        data=request.data
        data["communication_medium"] = "Call"
        data["phone_no"] = request.reciever_number

        
        await save_to_db(request.data)
    return response


@router.post("/send_mail")
async def send_mail_api(
    email: str = Form(...),  
    subject: str = Form(...),  
    message: str = Form(...),  
    data: str = Form(...),  
    attachments: Optional[List[UploadFile]] = File(None)
):
    import json
    try:
        parsed_data = json.loads(data)  
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format for 'data' field."}

    email_data = EmailRequest(email=email, subject=subject, message=message, data=parsed_data)

    response = await email_service.send_mail(email_data.email, email_data.subject, email_data.message, attachments)

    if response["status_code"] == 200:
        email_data.data["communication_medium"] = "Email"
        email_data.data["recipients"] = email_data.email
        email_data.data["subject"] = email_data.subject
        email_data.data["text_content"] = email_data.message

        await save_to_db(email_data.data)

    return response


# Whatsapp Integration
@router.post("/message_to_whatsapp")
async def send_whatsapp_message(request: WhatsAppRequest):
    response =  await whatsapp_service.send_whatsapp_message (request.message,request.phone_number)
    if response["status_code"]==200:
        data=request.data
        data["communication_medium"] = "WhatsApp"
        data["phone_no"] = request.phone_number
        await save_to_db(request.data)
    return response