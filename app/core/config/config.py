import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True
MONGODB_URL = os.getenv('DB_URL')
conn = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = conn[os.getenv('DB_NAME')]
SECRET_KEY = os.getenv('SECRET_KEY')