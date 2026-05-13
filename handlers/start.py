from config import config
from main import bot

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.menu import main_menu_kb
from database.supabase import get_user_field, upsert_user, add_loyalty_score_db
from utils.states import NameForm

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я — Штурман мастерской Art.El.\n\n"
        "Как я могу к тебе обращаться? (просто напиши имя)"
    )
    await state.set_state(NameForm.waiting_for_name)

@router.message(NameForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    
    if not name or len(name) < 2:
        await message.answer(
            "Как я могу к тебе обращаться?\n"
            "Напиши своё имя, пожалуйста 😊"
        )
        return

    user_id = message.from_user.id
    username = message.from_user.username
    existing_score = await get_user_field(user_id, 'loyalty_score') or 0

    await upsert_user(user_id, username, name)

    if existing_score == 0:
        await add_loyalty_score_db(user_id, 5)
        bonus_text = "\n\n⭐ +5 баллов за знакомство!"
    else:
        bonus_text = ""

    await state.clear()

    await message.answer(
        f"🎁 Отлично, <b>{name}</b>! У меня для тебя приятные новости:\n\n"
        "🎟️ Скидка <b>5%</b> уже активна (твой ранг: Новичок)\n"
        f"🕯️ И сувенир к первому заказу!{bonus_text}\n\n"
        "👇 <b>Смотри, что сейчас дарят по-настоящему:</b>",
        reply_markup=main_menu_kb(), parse_mode="HTML"
    )

@router.message(Command("ping"))
async def cmd_ping(message: types.Message):
    await message.reply("🏓 Понг!")

@router.message(Command("test_admin"))
async def test_admin_command(message: types.Message):
    user_id = message.from_user.id
    if user_id != config.ADMIN_ID:
        await message.reply("⛔ Только для админа.")
        return
    
    await message.reply("🔍 Проверяю доступ к админ-группе...")
    
    try:
        await bot.send_message(
            chat_id=config.ADMIN_GROUP_ID,
            text="✅ Тестовое сообщение от бота. Доступ есть!"
        )
        await message.reply("✅ Успешно! Уведомление отправлено в админ-группу.")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")

def register_start_handlers(dp):
    dp.include_router(router)
