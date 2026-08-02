from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
COUNTRY = os.getenv("COUNTRY")

if not APP_ID or not APP_KEY :
    raise ValueError("Adzuna credentials are missing. Check your .env file.")