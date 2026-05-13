import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import config
from handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook: {config.WEBHOOK_URL}/webhook")
    
    # Уведомление админу о запуске
    try:
        await bot.send_message(
            chat_id=config.ADMIN_GROUP_ID,
            text="🚀 <b>Бот запущен и готов к работе!</b>\n\n✅ Вебхук установлен\n✅ Планировщики активны"
        )
    except:
        pass

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    register_all_handlers(dp)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
