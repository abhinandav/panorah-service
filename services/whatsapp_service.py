from heyoo import WhatsApp
# from config.base import env_config

# WHATSAPP_NUMBER_ID = env_config.WHATSAPP_NUMBER_ID
# WHATSAPP_ACCOUNT_ID =  env_config.WHATSAPP_ACCOUNT_ID


WHATSAPP_ACCESS_TOKEN ="EAAHRy26iY3IBO1DdFvdMF4ZAxGrRfwsaWUzUnauP9kaZB2UrL544cIe6BuGWOvGRMW4DafKPDTjIIW3ZBUaNWDvoH9iIlZCB921ydCPxerIPOJIA0xyWq6wmIhZAcjRSSMBuuJo5ZC9Iv5BXNoZAyNMZA284GDi6gdYZCslFGaaebZBY2HLsY7dZBLlU7GRQu80MbW8lnMyqmZBczzQ0lRdIHUIL6py8Bz1fNOjpUjgZD"
WHATSAPP_NUMBER_ID = "487008924507078"
WHATSAPP_ACCOUNT_ID =  541311985734623

def send_whatsapp_message(message: str, phone_number: str):
    try:
        messenger = WhatsApp(WHATSAPP_ACCESS_TOKEN,WHATSAPP_NUMBER_ID)
        messenger.send_message(message, phone_number)
        return {"message": "✅ WhatsApp message sent successfully!", "status_code": 200}
    
    except Exception as e:
        raise RuntimeError({"message": f"⚠️ Failed to send WhatsApp message: {str(e)}", "status_code": 500})

 
message = "hai"
phone_number ="9207996045"
send_whatsapp_message(message,phone_number)