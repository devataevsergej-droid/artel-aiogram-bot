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
        "👋 Привет! Я Штурман мастерской четырёх стихий Art.El.\n\n"
        "Как я могу к тебе обращаться? (напиши имя)"
    )
    await state.set_state(NameForm.waiting_for_name)

@router.message(NameForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name or len(name) < 2:
        await message.answer("Пожалуйста, напиши имя (хотя бы 2 символа)")
        return

    user_id = message.from_user.id
    username = message.from_user.username

    await upsert_user(user_id, username, name)
    await add_loyalty_score_db(user_id, 5)

    await state.clear()

    await message.answer(
        f"🎁 Отлично, <b>{name}</b>! У меня для тебя приятные новости:\n\n"
        "🎟️ Скидка <b>5%</b> уже активна (твой ранг: Новичок)\n"
        "🕯️ И сувенир к первому заказу!\n\n"
        "👇 Смотри, что сейчас дарят по-настоящему:",
        reply_markup=main_menu_kb()
    )

@router.message(Command("ping"))
async def cmd_ping(message: types.Message):
    await message.reply("🏓 Понг!")

def register_start_handlers(dp):
    dp.include_router(router)
