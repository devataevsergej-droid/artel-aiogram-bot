from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import main_menu_kb
from database import get_user_field, upsert_user, add_loyalty_score

router = Router(name="start")

# Состояние для ожидания имени
class NameState(StatesGroup):
    waiting_for_name = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    name = get_user_field(uid, "name")
    
    if name and name not in [None, "None", "Друг"]:
        # Имя уже есть — показываем меню
        await message.answer(
            f"🧭 {name}, рад видеть снова!\n\n🔥 Смотри, что сейчас дарят:",
            reply_markup=main_menu_kb()
        )
    else:
        # Новый пользователь — спрашиваем имя
        await message.answer(
            "👋 Привет! Я Штурман Art.El.\n\n"
            "Как мне к тебе обращаться? (напиши имя)"
        )
        await state.set_state(NameState.waiting_for_name)

@router.message(NameState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name or len(name) < 2:
        await message.answer("Пожалуйста, напиши имя (хотя бы 2 буквы)")
        return
    
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Сохраняем пользователя
    upsert_user(user_id, username, name)
    
    # Проверяем, есть ли уже баллы (знакомились ли раньше)
    existing_score = get_user_field(user_id, "loyalty_score") or 0
    
    if existing_score == 0:
        add_loyalty_score(user_id, 5)
        bonus_text = "\n\n⭐ +5 баллов за знакомство!"
    else:
        bonus_text = ""
    
    await state.clear()
    
    await message.answer(
        f"🎁 Отлично, <b>{name}</b>! У меня для тебя приятные новости:\n\n"
        "🎟️ Скидка <b>5%</b> уже активна (твой ранг: Новичок)\n"
        f"🕯️ И сувенир к первому заказу!{bonus_text}\n\n"
        "👇 <b>Смотри, что сейчас дарят по-настоящему:</b>",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )

@router.message(Command("ping"))
async def cmd_ping(message: types.Message):
    await message.reply("🏓 Понг!")

def register_start_handlers(dp):
    dp.include_router(router)
