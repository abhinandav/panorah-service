import re
import asyncio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi import HTTPException
from config.base import env_config


PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

account_sid = env_config.TWILIO_ACCOUNT_SID
auth_token =  env_config.TWILIO_AUTH_TOKEN
twilio_number = env_config.TWILIO_NUMBER


async def send_sms(to_number: str, message_body: str)  -> dict:
    if not PHONE_REGEX.match(to_number):
        raise HTTPException(status_code=400, detail={"message": "❌ Invalid phone number format. Must be in international format (e.g., +919876543210)."})

    if not (1 <= len(message_body) <= 1600): 
        raise HTTPException(status_code=400, detail={"message": "❌ Message length must be between 1 and 1600 characters."})

    try:
        message = await asyncio.to_thread(
            lambda: Client(account_sid, auth_token).messages.create(
                from_=twilio_number,
                body=message_body,
                to=to_number
            )
        )
        return {"message": "✅ SMS sent successfully!", "message_sid": message.sid, "status_code": 200}

    except TwilioRestException as e:
        raise HTTPException(status_code=500, detail={"message": f"❌ Twilio API error: {e.msg}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"❌ Unexpected error: {str(e)}"})