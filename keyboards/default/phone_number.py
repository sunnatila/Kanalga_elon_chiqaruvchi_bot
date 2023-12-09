from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kontaktni yuborish", request_contact=True),
        ]
    ],
    resize_keyboard=True
)



