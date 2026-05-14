import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import config

# ========== 1. НАСТРОЙКИ ==========
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

from handlers import register_all_handlers
register_all_handlers(dp)

# ========== 2. ОБРАБОТЧИКИ ВЕБХУКА И HEALTHCHECK ==========
async def handle_webhook(request):
    """Принимает запросы от Telegram."""
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    return await handler.handle(request)

async def health_check(request):
    """Просто отвечает OK, чтобы Render не ругался."""
    return web.Response(text="OK", status=200)

# ========== 3. ФУНКЦИИ ЗАПУСКА И ОСТАНОВКИ ==========
async def on_startup(bot: Bot):
    """Устанавливает вебхук при старте бота."""
    webhook_url = f"{config.WEBHOOK_URL}/webhook"
    await bot.set_webhook(webhook_url)
    logging.info(f"✅ Вебхук установлен: {webhook_url}")

async def on_shutdown(bot: Bot):
    """Удаляет вебхук при остановке."""
    await bot.delete_webhook()
    logging.info("❌ Вебхук удалён")

# ========== 4. ЗАПУСК ПРИЛОЖЕНИЯ ==========
def main():
    app = web.Application()
    app.router.add_post("/webhook", handle_webhook)  # Главный путь для Telegram
    app.router.add_get("/", health_check)           # Для Render
    app.router.add_get("/health", health_check)     # Для Render

    # Связываем бота с приложением
    setup_application(app, dp, bot=bot)

    # Запускаем сервер
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
