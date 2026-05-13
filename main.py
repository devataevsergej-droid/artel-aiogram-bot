import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import config

# === ПРЯМОЙ ВЫВОД В ЛОГИ ===
print("🚀 ФАЙЛ main.py НАЧАЛ ЗАГРУЖАТЬСЯ!")
# ===========================

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

from handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)

# === ОБРАБОТЧИК ДЛЯ / (ОБЯЗАТЕЛЬНО) ===
async def handle_root(request):
    return web.Response(text="Bot is running", status=200)

# === ОБРАБОТЧИК ДЛЯ HEALTH CHECK ===
async def handle_health(request):
    return web.Response(text="OK", status=200)

async def on_startup(bot: Bot):
    print("✅ ФУНКЦИЯ on_startup ВЫЗВАНА!")
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook: {config.WEBHOOK_URL}/webhook")
    
    try:
        await bot.send_message(
            chat_id=-1003894573982,
            text="🚀 Бот запущен и готов к работе!\n\n✅ Вебхук установлен\n✅ Планировщики активны",
            parse_mode="HTML"
        )
        print("✅ Уведомление АДМИНУ УСПЕШНО ОТПРАВЛЕНО!")
    except Exception as e:
        print(f"❌ ОШИБКА при отправке: {e}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

def main():
    register_all_handlers(dp)
    
    app = web.Application()
    
    # Регистрируем обработчики для корня и health check
    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_health)
    
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
