import logging
import asyncio
from telegram import Update, ChatMember, Chat
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

# Hàm xử lý /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi là TagAll Bot 🤖. Gõ /tagall để tag mọi người trong nhóm.")

# Hàm xử lý /tagall
async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # Kiểm tra xem bot có đang hoạt động trong group không
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm.")
        return

    # Lấy danh sách thành viên (chỉ hoạt động với bot có quyền admin + trong nhóm public/supergroup)
    try:
        members = []
        async for member in context.bot.get_chat_administrators(chat.id):
            if not member.user.is_bot:
                members.append(member.user)
    except Exception as e:
        logger.error(f"Lỗi khi lấy thành viên nhóm: {e}")
        await update.message.reply_text("Không thể lấy danh sách thành viên. Hãy đảm bảo bot là admin.")
        return

    # Ghép tên để tag
    tag_text = " ".join([f"@{user.username}" if user.username else f"{user.first_name}" for user in members])

    if tag_text:
        await update.message.reply_text(f"Tag mọi người nè:\n{tag_text}")
    else:
        await update.message.reply_text("Không tìm thấy ai để tag.")

# Hàm main
async def main():
    app = ApplicationBuilder().token("8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA").build()

    # Xóa webhook cũ (nếu có)
    await app.bot.delete_webhook(drop_pending_updates=True)

    # Thêm các command handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tag_all))

    logger.info("Bot đang chạy...")
    await app.run_polling()

# Chạy main
if __name__ == '__main__':
    asyncio.run(main())
