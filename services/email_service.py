import smtplib
import os
import asyncio
import mimetypes
from email.message import EmailMessage

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_USER or not EMAIL_PASSWORD:
    raise ValueError("❌ Email credentials not found in environment variables!")

async def send_mail(email: str, subject: str, message: str, attachments: list | None = None):
    email_msg = EmailMessage()
    email_msg["From"] = EMAIL_USER
    email_msg["To"] = email
    email_msg["Subject"] = subject
    email_msg.set_content(message)

    if attachments:
        for attachment in attachments:
            try:
                file_data = await attachment.read()
                file_type, _ = mimetypes.guess_type(attachment.filename)
                file_type = file_type or "application/octet-stream"

                email_msg.add_attachment(
                    file_data,
                    maintype=file_type.split('/')[0],
                    subtype=file_type.split('/')[1],
                    filename=attachment.filename
                )
            except Exception as e:
                raise RuntimeError({"message": f"⚠️ Failed to attach {attachment.filename}: {e}", "status_code": 500})

    try:
        await asyncio.to_thread(send_email_sync, email_msg)
        return {"message": "✅ Email sent successfully!", "status_code": 200}

    except smtplib.SMTPAuthenticationError:
        raise ValueError({"message": "❌ Authentication failed! Check your email/password (use App Passwords if needed).", "status_code": 401})
    except smtplib.SMTPException as e:
        raise RuntimeError({"message": f"❌ Failed to send email: {e}", "status_code": 500})
    except Exception as e:
        raise RuntimeError({"message": f"⚠️ An unexpected error occurred: {e}", "status_code": 500})
    

    
def send_email_sync(email_msg):
    """
    Synchronous function to send email using SMTP.
    This is executed in a separate thread using asyncio.to_thread().

    :param email_msg: The prepared email message
    """
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  
        server.login(EMAIL_USER, EMAIL_PASSWORD)  
        server.send_message(email_msg)  


