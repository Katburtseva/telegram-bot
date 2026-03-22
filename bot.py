import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# СЮДА ВСТАВЬ СВОЙ ТОКЕН (между кавычками)
BOT_TOKEN = "8372379665:AAFjHFztodzZTBz8gBVSrhECQmx9CTjoHeI"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Напиши любое слово или фразу, и я скажу, "
        "на сколько процентов это про тебя!\n\n"
    )


async def percent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = random.randint(0, 100)

    if value <= 20:
        emoji = "😢"
    elif value <= 40:
        emoji = "😐"
    elif value <= 60:
        emoji = "🙂"
    elif value <= 80:
        emoji = "😊"
    else:
        emoji = "🔥"

    await update.message.reply_text(f"🎲 Твой результат: {value}% {emoji}")


async def random_percent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    value = random.randint(0, 100)

    if value <= 20:
        emoji = "😢"
    elif value <= 40:
        emoji = "😐"
    elif value <= 60:
        emoji = "🙂"
    elif value <= 80:
        emoji = "😊"
    else:
        emoji = "🔥"

    await update.message.reply_text(
        f"❓ «{text}»\n\nОтвет: {value}% {emoji}"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("percent", percent))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_percent_message))

    print("✅ Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
