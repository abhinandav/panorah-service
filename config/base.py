from dataclasses import dataclass
import os

from dotenv import load_dotenv
load_dotenv()


@dataclass
class EnvSettings:
	"""Communication configurations."""
	TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
	TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
	TWILIO_NUMBER: str = os.getenv("TWILIO_NUMBER", "")
	SERVER_URL:str =os.getenv("SERVER_URL","")
	EMAIL_USER:str =os.getenv("EMAIL_USER","")
	EMAIL_PASSWORD:str =os.getenv("EMAIL_PASSWORD","")

	WHATSAPP_ACCOUNT_ID:str =os.getenv("WHATSAPP_ACCOUNT_ID","")
	WHATSAPP_NUMBER_ID:str =os.getenv("EMAIL_PASSWORD","")
	
	DB_NAME:str =os.getenv("DB_NAME","")
	DB_USER:str =os.getenv("DB_USER","postgres")
	DB_PASSWORD:str =os.getenv("DB_PASSWORD","")
	DB_HOST:str =os.getenv("DB_HOST","localhost")
	DB_PORT:str =os.getenv("DB_PORT","5432")
	DB_ENGINE:str =os.getenv("DB_ENGINE","postgresql")

	
	
env_config = EnvSettings()
