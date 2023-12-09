from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.phone_or_computer import phone_or_comp
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!\n"
                         f"Elon berish uchun kategoriyani tanlang.", reply_markup=phone_or_comp)
