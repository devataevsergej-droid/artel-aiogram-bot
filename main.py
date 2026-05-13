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

# === ОБРАБОТЧИК ВЕБХУКА (БЕЗ УВЕДОМЛЕНИЯ) ===
async def webhook_handler(request):
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
    app.router.add_post("/webhook", webhook_handler)
    
    async def health(request):
        return web.Response(text="OK", status=200)
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
