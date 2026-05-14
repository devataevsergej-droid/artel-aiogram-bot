from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Посмотреть, что сейчас дарят", callback_data="bonus")],
        [InlineKeyboardButton(text="👥 Личный кабинет", callback_data="profile")],
        [InlineKeyboardButton(text="🏆 Доска почёта (ТОП-10)", callback_data="top_referrals")],
        [InlineKeyboardButton(text="📢 Канал Art.El", url="https://t.me/artelena_test")]
    ])
    return kb