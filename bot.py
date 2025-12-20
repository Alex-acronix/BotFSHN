import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = "8383502918:AAEo3ofVGWgGU_vaT41_JYgacl_4g5fwJ4A"
ADMIN_ID = 1295790888  # твій Telegram ID

NAME, FACULTY, COURSE, MOTIVATION = range(4)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! 👋\n"
        "Це бот набору в раду студентського самоврядування.\n\n"
        "Як тебе звати?"
    )
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("На якій спеціальності ви навчаєтесь?")
    return FACULTY

async def faculty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["faculty"] = update.message.text
    await update.message.reply_text("З якого ви курсу?")
    return COURSE

async def course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["course"] = update.message.text
    await update.message.reply_text("Чому хочеш вступити до ради студентського самоврядування?")
    return MOTIVATION

async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["motivation"] = update.message.text

    user = update.effective_user
    text = (
        "📥 Нова заявка:\n\n"
        f"👤 Ім’я: {context.user_data['name']}\n"
        f"🏫 Спеціальність: {context.user_data['faculty']}\n"
        f"🎓 Курс: {context.user_data['course']}\n"
        f"💬 Мотивація: {context.user_data['motivation']}\n"
        f"🔗 Telegram: @{user.username}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await update.message.reply_text("Дякуємо! Твоя заявка надіслана ✅")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заповнення скасовано.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            FACULTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, faculty)],
            COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, course)],
            MOTIVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, motivation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()