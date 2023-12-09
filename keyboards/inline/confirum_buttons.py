from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

phone_callback_data = CallbackData('confirm', 'action')

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash", callback_data=phone_callback_data.new(action='post')),
            InlineKeyboardButton(text="Rad etish", callback_data=phone_callback_data.new(action='cancel'))
        ]
    ]
)

