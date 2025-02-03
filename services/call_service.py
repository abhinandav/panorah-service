import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_NUMBER")


async def initiate_call(recipient_phone_number: str):
    if not all([ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        raise ValueError({"message": "❌ Missing Twilio credentials. Check your .env file.", "status_code": 500})
    
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        call = client.calls.create(
            twiml=f"<Response><Dial>{recipient_phone_number}</Dial></Response>",
            to=recipient_phone_number,
            from_=TWILIO_PHONE_NUMBER
        )
        return {"message": "📞 Call initiated successfully!", "call_sid": call.sid, "status_code": 200}

    except TwilioRestException as e:
        raise RuntimeError({"message": f"❌ Twilio API Error: {e.msg}", "status_code": e.status})
    except ValueError:
        raise ValueError({"message": "❌ Invalid phone number format.", "status_code": 400})
    except Exception as e:
        raise RuntimeError({"message": f"⚠️ Unexpected error occurred: {str(e)}", "status_code": 500})
