import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

DATA_FILE = "users.json"

def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.full_name
    users = load_users()
    if username not in users:
        users.append(username)
        save_users(users)
        await update.message.reply_text(f"✅ Đã đăng ký: {username}")
    else:
        await update.message.reply_text(f"Bạn đã đăng ký rồi, {username}!")

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    if not users:
        await update.message.reply_text("⚠️ Chưa có ai đăng ký.")
        return
    tags = " ".join(users)
    await update.message.reply_text(f"📣 Gọi cả nhóm:\n{tags}")

async def start_bot():
    import os
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", register))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("tagall", tag_all))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())
