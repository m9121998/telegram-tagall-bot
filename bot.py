import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Đăng nhập log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Danh sách member_id lưu tạm
member_ids = set()

# Khi bot khởi động hoặc khi lệnh /start được gọi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đã sẵn sàng. Dùng /tagall để tag mọi người!")

# Hàm khi bot nhận thành viên mới
async def collect_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if not member.is_bot:
            member_ids.add(member.id)
            logger.info(f"Đã thêm thành viên: {member.full_name} (ID: {member.id})")

# Hàm /tagall
async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Lệnh này chỉ dùng trong nhóm.")
        return

    tags = []
    for user_id in member_ids:
        try:
            member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            user = member.user
            if not user.is_bot:
                if user.username:
                    tags.append(f"@{user.username}")
                else:
                    name = user.full_name.replace("[", "").replace("]", "")
                    tags.append(f"[{name}](tg://user?id={user.id})")
        except Exception as e:
            logger.warning(f"Không lấy được thành viên {user_id}: {e}")

    if tags:
        tag_text = "Tag tất cả nè:\n" + "\n".join(tags)
        await update.message.reply_text(tag_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("Chưa có ai để tag 😅. Hãy để mọi người tương tác trước.")

# Hàm chính để chạy bot
async def main():
    TOKEN = os.getenv("BOT_TOKEN") or "8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA"
    app = Application.builder().token(TOKEN).build()

    # Xóa webhook nếu đang deploy ở môi trường hỗ trợ polling (như local)
    await app.bot.delete_webhook()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tag_all))
    app.add_handler(CommandHandler("restart", start))
    app.add_handler(CommandHandler("help", start))

    # Lắng nghe thành viên mới
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, collect_members))

    logger.info("Bot đang chạy...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
