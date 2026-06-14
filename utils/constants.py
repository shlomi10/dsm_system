import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")

API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "Aa123456")

RESOLUTION_COMMENT = "Remediation verified successfully and issue is resolved"
