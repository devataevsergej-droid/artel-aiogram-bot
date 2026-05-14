from aiogram import F, Router, types
from keyboards import main_menu_kb, back_to_main_kb

router = Router(name="menu")

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🧭 Главное меню",
        reply_markup=main_menu_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "bonus")
async def bonus(callback: types.CallbackQuery):
    text = "🔥 Смотри, что сейчас дарят:\n\n👇 Выбери вариант:"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("👀 Посмотреть идеи", callback_data="spy"))
    kb.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_main"))
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "spy")
async def spy(callback: types.CallbackQuery):
    text = "👀 Подборка лучших идей:\n\n👇 Выбери свой вариант:"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎁 Подобрать подарок", callback_data="quiz"))
    kb.add(types.InlineKeyboardButton("◀️ Назад", callback_data="bonus"))
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "quiz")
async def quiz(callback: types.CallbackQuery):
    text = "🎯 Квиз: кто будет радоваться подарку?\n\nНапиши в чат (мама, девушка, друг...)"
    await callback.message.edit_text(text, reply_markup=back_to_main_kb())
    await callback.answer()

def register_menu_handlers(dp):
    dp.include_router(router)

@router.callback_query(lambda c: c.data == "profile")
async def temp_profile(callback: types.CallbackQuery):
    await callback.message.answer("✅ Временный профиль. Если это сообщение пришло — кнопка работает!")
    await callback.answer()
