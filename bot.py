import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Cấu hình log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi là TagAll Bot 🤖")

# Hàm main để khởi chạy bot
async def main():
    # Tạo ứng dụng với token Telegram Bot của bạn
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    # Xóa webhook cũ (nếu có)
    await app.bot.delete_webhook(drop_pending_updates=True)

    # Thêm command handler
    app.add_handler(CommandHandler("start", start))

    # Chạy bot (lắng nghe update từ Telegram)
    logger.info("Bot đang chạy...")
    await app.run_polling()

# Gọi hàm main bằng asyncio
if __name__ == '__main__':
    asyncio.run(main())
