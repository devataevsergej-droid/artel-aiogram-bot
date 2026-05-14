from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config

def main_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Посмотреть, что сейчас дарят", callback_data="bonus")],
        [InlineKeyboardButton(text="👥 Личный кабинет", callback_data="profile")],
        [InlineKeyboardButton(text="🏆 Доска почёта (ТОП-10)", callback_data="top_referrals")],
        [InlineKeyboardButton(text="📢 Канал Art.El", url=config.CHANNEL_URL)]
    ])
    return kb

def back_to_main_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="◀️ В главное меню", callback_data="back_to_main"))
    return kb
