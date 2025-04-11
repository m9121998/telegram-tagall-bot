import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Xin chào! Tôi là bot gắn thẻ nhóm.")

# Command: /tagall
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    members = await context.bot.get_chat_administrators(chat.id)
    tags = ""

    for member in members:
        user = member.user
        if user.username:
            tags += f"@{user.username} "
        else:
            tags += f"[{user.first_name}](tg://user?id={user.id}) "

    await update.message.reply_text(tags, parse_mode='Markdown')

# Hàm chạy bot (không cần asyncio.run)
async def main():
    app = ApplicationBuilder().token("8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tagall))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# Kiểm tra nếu chạy trực tiếp file thì chạy bot
if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        # fallback nếu event loop đã chạy (Render hoặc notebook)
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
