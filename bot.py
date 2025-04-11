import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import asyncio

# Cấu hình log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hàm xử lý /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi là TagAll Bot 🤖. Gõ /tagall để tag mọi người trong nhóm.")

# Hàm xử lý /tagall
async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm.")
        return

    try:
        members = []
        async for member in context.bot.get_chat_administrators(chat.id):
            if not member.user.is_bot:
                members.append(member.user)
    except Exception as e:
        logger.error(f"Lỗi khi lấy thành viên nhóm: {e}")
        await update.message.reply_text("Không thể lấy danh sách thành viên. Hãy đảm bảo bot là admin.")
        return

    tag_text = " ".join([f"@{user.username}" if user.username else user.first_name for user in members])
    if tag_text:
        await update.message.reply_text(f"Tag mọi người nè:\n{tag_text}")
    else:
        await update.message.reply_text("Không tìm thấy ai để tag.")

# Chạy app trong môi trường đã có event loop (Render, Jupyter, v.v.)
def main():
    app = ApplicationBuilder().token("8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tag_all))

    logger.info("Bot đang chạy...")
    app.run_polling()  # Không dùng asyncio.run nữa

if __name__ == '__main__':
    main()
