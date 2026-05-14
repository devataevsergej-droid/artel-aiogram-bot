from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.supabase import get_user_field

router = Router(name="profile")

def get_progress_bar(score: int, next_score: int) -> str:
    """Возвращает текстовый прогресс-бар (10 символов)"""
    if next_score <= 0:
        return "█" * 10
    filled = int(10 * score / next_score)
    return "█" * filled + "░" * (10 - filled)

@router.callback_query(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    # Получаем данные пользователя
    name = await get_user_field(user_id, "name") or "Друг"
    rank = await get_user_field(user_id, "loyalty_rank") or "Новичок"
    score = await get_user_field(user_id, "loyalty_score") or 0
    
    # Пороги рангов
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
        f"👋 Привет, {name}!\n"
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
