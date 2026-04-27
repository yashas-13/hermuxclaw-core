# core/config.py
import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

class Config:
    HX_PORT = int(os.getenv("HX_PORT", 8013))
    DB_PATH = os.getenv("HX_DB_PATH", "memory/registry.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Client Specific
    SAP_URL = os.getenv("SAP_URL")
    WA_TOKEN = os.getenv("WA_TOKEN")
    WA_PHONE_ID = os.getenv("WA_PHONE_ID")
    ZOHO_TOKEN = os.getenv("ZOHO_TOKEN")
    OPENAI_KEY = os.getenv("OPENAI_KEY")

config = Config()
