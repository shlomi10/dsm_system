import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")

API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "Aa123456")

LOGIN_ENDPOINT = "/api/login"
HEALTH_ENDPOINT = "/api/health"
POLICY_CONFIG_ENDPOINT = "/api/policy-config"
SCANS_ENDPOINT = "/api/scans"
ALERTS_ENDPOINT = "/api/alerts"
RESET_ENDPOINT = "/api/admin/reset"

RESOLUTION_COMMENT = "Remediation verified successfully and issue is resolved"
