import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ChatMemberHandler
)

# Cấu hình log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Tạm thời lưu ID thành viên trong bộ nhớ RAM
member_ids = set()

# Lưu thành viên khi họ gửi tin nhắn
async def save_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        user = update.effective_user
        if not user.is_bot:
            member_ids.add(user.id)

# Lưu thành viên khi họ vào nhóm
async def track_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member.new_chat_member
    if not member.user.is_bot:
        member_ids.add(member.user.id)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi sẽ ghi nhớ thành viên và có thể tag tất cả bằng /tagall.")

# Lệnh /tagall
async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Lệnh này chỉ dùng được trong nhóm.")
        return

    tags = []
    for user_id in member_ids:
        try:
            member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            if not member.user.is_bot:
                if member.user.username:
                    tags.append(f"@{member.user.username}")
                else:
                    tags.append(f"{member.user.first_name}")
        except Exception as e:
            logger.warning(f"Không lấy được thông tin thành viên {user_id}: {e}")

    if tags:
        tag_text = " ".join(tags)
        await update.message.reply_text(f"Tag tất cả nè:\n{tag_text}")
    else:
        await update.message.reply_text("Chưa có ai để tag 😅. Hãy để mọi người tương tác trước.")

# Hàm main chạy bot
def main():
    app = ApplicationBuilder().token("8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tag_all))

    # Theo dõi tin nhắn & thành viên mới
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_user))
    app.add_handler(ChatMemberHandler(track_new_member, ChatMemberHandler.CHAT_MEMBER))

    logger.info("Bot đang chạy...")
    app.run_polling()

if __name__ == '__main__':
    main()
