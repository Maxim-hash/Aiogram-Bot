from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "/start"),
            KeyboardButton(text = "/test")
        ], 
        [
            KeyboardButton(text = "/lang"), 
            KeyboardButton(text = "/records")
        ]
    ], 
    resize_keyboard = True
)

lang_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "/edit")
        ], 
        [
            KeyboardButton(text = "/return")
        ]
    ], 
    resize_keyboard = True
)

inline_lang_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "Russian", callback_data="Russian:rus")
        ],
        [
            InlineKeyboardButton(text = "English", callback_data="English:eng")
        ]
    ]
)