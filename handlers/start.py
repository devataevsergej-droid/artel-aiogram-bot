from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.menu import main_menu_kb
from database.supabase import get_user_field, upsert_user, log_action
from utils.states import NameForm

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await log_action(message.from_user.id, "start")
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

    await upsert_user(user_id, username, name)

    await state.clear()

    await message.answer(
        f"🎁 Отлично, <b>{name}</b>! У меня для тебя приятные новости:\n\n"
        "🎟️ Скидка <b>5%</b> уже активна (твой ранг: Новичок)\n"
        "🕯️ И сувенир к первому заказу!\n\n"
        "👇 <b>Смотри, что сейчас дарят по-настоящему:</b>",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )

@router.message(Command("ping"))
async def cmd_ping(message: types.Message):
    await message.reply("🏓 Понг!")

def register_start_handlers(dp):
    dp.include_router(router)
