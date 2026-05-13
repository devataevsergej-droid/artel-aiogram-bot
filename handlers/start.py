from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from keyboards import main_menu_kb
from database import get_user_field

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    uid = message.from_user.id
    name = get_user_field(uid, "name")
    
    if name and name not in [None, "None", "Друг"]:
        text = f"🧭 {name}, рад видеть снова!\n\n🔥 Смотри, что сейчас дарят:"
        await message.answer(text, reply_markup=main_menu_kb())
    else:
        await message.answer(
            "👋 Привет! Я Штурман Art.El.\n\n"
            "Как мне к тебе обращаться? (напиши имя)"
        )

@router.message(Command("ping"))
async def cmd_ping(message: types.Message):
    await message.reply("🏓 Понг!")

def register_start_handlers(dp):
    dp.include_router(router)