import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

from handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)

# === ФЛАГ ДЛЯ ОДНОКРАТНОЙ ОТПРАВКИ ===
startup_notified = False

# === ОСНОВНОЙ ОБРАБОТЧИК ВЕБХУКА ===
async def webhook_handler(request):
    global startup_notified
    
    # Отправляем уведомление при первом обращении к вебхуку
    if not startup_notified:
        try:
            await bot.send_message(
                chat_id=-1003894573982,
                text="🚀 <b>Бот запущен и готов к работе!</b>\n\n✅ Вебхук активен\n✅ Бот принимает запросы",
                parse_mode="HTML"
            )
            startup_notified = True
            logging.info("✅ Уведомление отправлено через вебхук")
        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")
    
    # Передаём запрос дальше
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    return await handler.handle(request)

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook: {config.WEBHOOK_URL}/webhook")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

def main():
    register_all_handlers(dp)
    
    app = web.Application()
    
    # Регистрируем обработчик вебхука
    app.router.add_post("/webhook", webhook_handler)
    
    # Health check
    async def health(request):
        return web.Response(text="OK", status=200)
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
