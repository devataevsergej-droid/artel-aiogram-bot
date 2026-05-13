import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import config

# ========== 1. СНАЧАЛА СОЗДАЁМ bot И dp ==========
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# ========== 2. ПОТОМ ИМПОРТИРУЕМ handlers ==========
from handlers import register_all_handlers

# ========== 3. НАСТРАИВАЕМ ЛОГИРОВАНИЕ ==========
logging.basicConfig(level=logging.INFO)

# ========== 4. ФУНКЦИИ ЗАПУСКА И ОСТАНОВКИ ==========
async def on_startup(bot: Bot):
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook: {config.WEBHOOK_URL}/webhook")
    
    # Уведомление админу (рабочий код из test_admin)
    try:
        await bot.send_message(
            chat_id=-1003894573982,  # Твой ADMIN_GROUP_ID
            text="🚀 <b>Бот запущен и готов к работе!</b>\n\n✅ Вебхук установлен\n✅ Планировщики активны",
            parse_mode="HTML"
        )
        logging.info("✅ Уведомление админу отправлено успешно!")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке уведомления: {e}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

# ========== 5. ГЛАВНАЯ ФУНКЦИЯ ==========
def main():
    register_all_handlers(dp)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
