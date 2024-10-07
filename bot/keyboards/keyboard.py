from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
                                    [KeyboardButton(text="Start monitoring"),
                                     KeyboardButton(text="Stop monitoring")],
                                    [KeyboardButton(text="Set min %"),
                                     KeyboardButton(text="Set max %")],
                                    [KeyboardButton(text="Add streamer"),
                                     KeyboardButton(text="Delete streamer")],
                                    [KeyboardButton(text="My Streamers")]
                                    ],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')
