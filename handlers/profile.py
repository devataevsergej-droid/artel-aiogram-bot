from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.supabase import get_user_rank
from keyboards.menu import main_menu_kb

router = Router(name="profile")

def get_progress_bar(score: int, next_rank_score: int) -> str:
    """Возвращает текстовый прогресс-бар"""
    if next_rank_score <= 0:
        return "█" * 10
    filled = int(10 * score / next_rank_score)
    return "█" * filled + "░" * (10 - filled)

@router.callback_query(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    user_data = await get_user_rank(user_id)
    rank = user_data.get("loyalty_rank", "Новичок")
    score = user_data.get("loyalty_score", 0)
    
    # Пороги для рангов
    rank_thresholds = {
        "Новичок": 0,
        "Путник": 500,
        "Искатель": 1000,
        "Знаток": 2000,
        "Мастер": 4000,
        "Профи": 7000,
        "Легенда": 10000
    }
    
    # Находим следующий ранг
    next_rank = None
    next_score = 0
    for r, s in rank_thresholds.items():
        if s > score:
            next_rank = r
            next_score = s
            break
    
    if next_rank:
        progress_bar = get_progress_bar(score, next_score)
        progress_text = f"\n\n⭐ До ранга **{next_rank}** осталось **{next_score - score}** баллов\n{progress_bar} {score}/{next_score}"
    else:
        progress_text = "\n\n🏆 Вы достигли **высшего ранга**! Поздравляем!"
    
    text = (
        f"👤 **ЛИЧНЫЙ КАБИНЕТ**\n\n"
        f"🏆 Ранг: **{rank}**\n"
        f"⭐ Баллы: **{score}**{progress_text}\n\n"
        "👇 Доступные разделы:"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Мои рефералы", callback_data="referrals")],
        [InlineKeyboardButton(text="❤️ Избранное", callback_data="favorites")],
        [InlineKeyboardButton(text="🛒 Моя корзина", callback_data="cart")],
        [InlineKeyboardButton(text="📅 Мои праздники", callback_data="holidays")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()
