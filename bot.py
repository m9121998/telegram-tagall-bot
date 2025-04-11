import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from collections import defaultdict

# Bật log để debug nếu cần
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Biến toàn cục để lưu danh sách người dùng theo group_id
user_data = defaultdict(set)

# Xử lý khi người dùng gửi /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi là bot gắn thẻ nhóm.")

# Xử lý khi có ai đó gửi tin nhắn => lưu user vào danh sách
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type in ['group', 'supergroup']:
        group_id = update.message.chat_id
        user = update.message.from_user

        # Thêm user vào danh sách theo group_id
        user_data[group_id].add((user.id, user.full_name))
        logging.info(f"Đã lưu user {user.full_name} vào nhóm {group_id}")

# Lệnh /tagall
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat_id
    if group_id not in user_data or not user_data[group_id]:
        await update.message.reply_text("Chưa có ai tương tác để tag cả 😢")
        return

    tag_message = ""
    for user_id, full_name in user_data[group_id]:
        tag_message += f"[{full_name}](tg://user?id={user_id}) "

    await update.message.reply_text(tag_message, parse_mode='Markdown')

# Chạy bot
async def main():
    app = ApplicationBuilder().token("8179738384:AAEgHjuelNihVY2tZYMG4aOz5iUZjvEeOeA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tagall))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), track_users))

    logging.info("Bot đang chạy...")
    await app.delete_webhook(drop_pending_updates=True)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
