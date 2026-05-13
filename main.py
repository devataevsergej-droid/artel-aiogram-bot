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

# Флаг для ОДНОКРАТНОЙ отправки уведомления
notification_sent = False

# === ОБРАБОТЧИК ВЕБХУКА (С УВЕДОМЛЕНИЕМ) ===
async def handle_webhook(request):
    global notification_sent
    
    # Отправляем уведомление ПРИ ПЕРВОМ обращении к вебхуку
    if not notification_sent:
        try:
            await bot.send_message(
                chat_id=-1003894573982,
                text="🚀 <b>Бот запущен и готов к работе!</b>\n\n✅ Вебхук активен\n✅ Бот принимает запросы",
                parse_mode="HTML"
            )
            notification_sent = True
            logging.info("✅ Уведомление отправлено через вебхук")
        except Exception as e:
            logging.error(f"❌ Ошибка отправки: {e}")
    
    # Передаём запрос в aiogram
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    return await handler.handle(request)

# === ВСПОМОГАТЕЛЬНЫЕ ОБРАБОТЧИКИ ===
async def handle_root(request):
    return web.Response(text="Bot is running", status=200)

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook: {config.WEBHOOK_URL}/webhook")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

def main():
    register_all_handlers(dp)
    
    app = web.Application()
    app.router.add_post("/webhook", handle_webhook)  # <--- ВЕБХУК С УВЕДОМЛЕНИЕМ
    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_root)
    
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
