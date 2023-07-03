import os
from dotenv import load_dotenv

load_dotenv()

# Store link
STORE = os.getenv("STORE", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "")

# Oath
APPKEY = os.getenv("APPKEY", "")
APPTOKEN = os.getenv("APPTOKEN", "")

# S3
S3_BUCKET = os.getenv("S3_BUCKET", "")
