import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import config

# === ПРЯМОЙ ВЫВОД В ЛОГИ ДЛЯ ПРОВЕРКИ ===
print("🚀 ФАЙЛ main.py НАЧАЛ ЗАГРУЖАТЬСЯ!")
# =======================================

# Создаём bot и dp
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

from handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)

async def on_startup(bot: Bot):
    print("✅ ФУНКЦИЯ on_startup ВЫЗВАНА!") # <-- ЭТО ВАЖНОЕ СООБЩЕНИЕ
    
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook: {config.WEBHOOK_URL}/webhook")
    
    # Отправляем уведомление
    try:
        await bot.send_message(
            chat_id=-1003894573982,
            text="🚀 Бот запущен и готов к работе!\n\n✅ Вебхук установлен\n✅ Планировщики активны"
        )
        print("✅ Уведомление АДМИНУ УСПЕШНО ОТПРАВЛЕНО!") # <-- ЭТО ВАЖНОЕ СООБЩЕНИЕ
        logging.info("✅ Уведомление админу отправлено успешно!")
    except Exception as e:
        print(f"❌ ОШИБКА при отправке: {e}") # <-- ЭТО ВАЖНОЕ СООБЩЕНИЕ
        logging.error(f"❌ Ошибка при отправке уведомления: {e}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

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
