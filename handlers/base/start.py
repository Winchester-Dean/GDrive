import os.path
import utils
import logging

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import DataBase
from dispatcher import dp, router
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

db = DataBase()

class Form(StatesGroup):
    link = State()

@router.message(Command('start'))
async def start(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admins = db.get_admins_id()
    
    if (user_id,) not in admins:
        return await msg.answer("Вы не имеете право пользоваться ботом!")

    await state.set_state(Form.link)
    await msg.answer("Привет! Введите ссылку чтобы бот начал обработку:")

@dp.message(Form.link)
async def handle_link(msg: Message, state: FSMContext):
    link = msg.text
    domains = db.get_domains()

    parsed_url = urlparse(link)
    domain = parsed_url.netloc

    if (domain,) not in domains:
        return await msg.answer("Ваша ссылка или домен не поддерживается!")
    
    await msg.answer("Начинаю обработку ссылки...")

    url = link + "/info"
    links = utils.get_links(url)

    upload_file = utils.upload_file("subscription.txt", "Subscription")

    await msg.answer(
        "Вот ваша ссылка подписки:\n"
        f"https://drive.google.com/uc?id{upload_file}&export=download"
    )

