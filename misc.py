from os import environ
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
REQUIRED_ENV = ['OWNER_TOKEN']

for var in REQUIRED_ENV:
    if var not in environ:
        raise EnvironmentError(f"{var} is not set.")

BOT_TOKEN = environ.get('OWNER_TOKEN')

bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()  # TODO: More persistent storage, maybe?
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)
