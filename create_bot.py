from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    logging.error("API_TOKEN not found in .env file!")
else:
    logging.info("API_TOKEN loaded successfully.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()