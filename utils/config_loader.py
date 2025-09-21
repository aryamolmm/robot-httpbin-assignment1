from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("BASE_URL", "https://httpbin.org")
TIMEOUT = int(os.getenv("TIMEOUT", 10))
RETRY = int(os.getenv("RETRY", 3))
