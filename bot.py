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
ADMIN_IDS = [1295790888, 937454085, 730833899, 2112719948, 725297705]

(
    NAME,
    COURSE_SPECIALTY,
    CONTACT,
    INTERESTS,
    MOTIVATION
) = range(5)

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋\n"
        "Ти у чатботі Ради студентського самоврядування ФСГН\n\n"
        "Якщо ти хочеш впливати на життя факультету, брати участь у подіях, "
        "ініціативах та реальних змінах — ти точно за адресою\n\n"
        "Готовий(а) долучитися? Тоді давай знайомитися 👇"
    )

    await update.message.reply_text(
        "РСС — це не «для галочки».\n"
        "Це про:\n"
        "• голос студентів\n"
        "• команду\n"
        "• ідеї, які реально реалізуються\n"
        "• досвід, що працює в резюме\n\n"
        "Заповнення займе 2–3 хвилини.\n\n"
        "Для початку напиши, будь ласка:\n\n"
        "1️⃣ Ім’я та прізвище\n"
        "(як до тебе звертатися)"
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "2️⃣ Курс та спеціальність\n"
        "(наприклад: 2 курс, політологія)"
    )
    return COURSE_SPECIALTY


async def course_specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["course_specialty"] = update.message.text
    await update.message.reply_text(
        "3️⃣ Контакт для зв’язку\n"
        "Telegram / Instagram / номер телефону\n"
        "(той, де ти точно відповідаєш)"
    )
    return CONTACT


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text(
        "4️⃣ Що тобі найбільше цікаво?\n"
        "Можеш обрати одне або кілька:\n\n"
        "• організація заходів\n"
        "• комунікації / соцмережі\n"
        "• робота з першокурсниками\n"
        "• проєкти, волонтерство\n"
        "• захист прав студентів\n"
        "• ще не знаю, але хочу спробувати\n\n"
        "(просто напиши варіант)"
    )
    return INTERESTS


async def interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["interests"] = update.message.text
    await update.message.reply_text(
        "5️⃣ Чому ти хочеш долучитися до РСС?\n"
        "Можна коротко. Тут без «правильних» відповідей)"
    )
    return MOTIVATION


async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["motivation"] = update.message.text

    user = update.effective_user
    text = (
        "📥 Нова заявка до РСС ФСГН:\n\n"
        f"👤 Ім’я: {context.user_data['name']}\n"
        f"🎓 Курс і спеціальність: {context.user_data['course_specialty']}\n"
        f"📞 Контакт: {context.user_data['contact']}\n"
        f"⭐ Інтереси: {context.user_data['interests']}\n"
        f"💬 Мотивація: {context.user_data['motivation']}\n"
        f"🔗 Telegram: @{user.username}"
    )

    for admin_id in ADMIN_IDS:
        await context.bot.send_message(chat_id=admin_id, text=text)

    await update.message.reply_text(
        "Дякую 🤍\n"
        "Твоя відповідь прийнята\n\n"
        "Ми зв’яжемося з тобою найближчим часом і розкажемо про наступні кроки\n"
        "Рада студентського самоврядування — це про людей, які не бояться брати відповідальність\n\n"
        "До зв’язку 👀✨"
    )

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
            COURSE_SPECIALTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, course_specialty)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, contact)],
            INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, interests)],
            MOTIVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, motivation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()


if __name__ == "__main__":
    main()


