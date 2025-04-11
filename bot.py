import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

# Main function (chạy bot)
def main():
    app = ApplicationBuilder().token("8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tagall))

    app.run_polling()

if __name__ == '__main__':
    main()
