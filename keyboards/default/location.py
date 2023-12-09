from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="lokatsiyani yuborish", request_location=True),
        ]
    ],
    resize_keyboard=True
)






