from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_or_comp = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon sotish"),
            KeyboardButton(text="Kompyuter sotish")
        ]
    ],
    resize_keyboard=True
)



