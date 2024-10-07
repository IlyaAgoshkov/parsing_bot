from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.keyboards.keyboard import main

start_router = Router()


@start_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main)
