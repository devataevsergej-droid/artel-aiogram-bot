from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config

def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔥 Смотреть подарки", callback_data="bonus"),
        InlineKeyboardButton("👥 Личный кабинет", callback_data="profile"),
        InlineKeyboardButton("🎬 Конкурс", callback_data="contest"),
        InlineKeyboardButton("📢 Канал", url=config.CHANNEL_URL)
    )
    return kb

def back_to_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main"))
    return kb