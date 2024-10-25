import logging

import markovify
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

from asyncpg_lite import DatabaseManager




all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')

with open(os.path.join(all_media_dir, "che.txt"), encoding="utf8") as f:
    text = f.read()

text_model = markovify.Text(text)

#from db_handler.db_class import PostgresHandler

#pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

pg_manager = DatabaseManager(db_url=config("PG_LINK"), deletion_password=config("ROOT_PASS"))
redis_url = config('REDIS_URL')
