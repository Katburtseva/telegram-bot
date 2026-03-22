import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8372379665:AAFjHFztodzZTBz8gBVSrhECQmx9CTjoHeI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!\n\n"
        "Напиши любое слово или фразу, и я скажу, "
        "на сколько процентов это про тебя!\n\n"
    )

async def percent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = random.randint(0, 100)
    if value <= 20:
        emoji = "sad"
    elif value <= 40:
        emoji = "ok"
    elif value <= 60:
        emoji = "good"
    elif value <= 80:
        emoji = "great"
    else:
        emoji = "fire"
    await update.message.reply_text(f"Result: {value}% {emoji}")

async def random_percent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text
    bot_username = context.bot.username

    if message.chat.type in ["group", "supergroup"]:
        mention = "@" + bot_username
        if mention.lower() not in text.lower():
            return
        text = text.replace(mention, "").strip()
        if not text:
            text = "это"

    value = random.randint(0, 100)
    if value <= 20:
        emoji = "sad"
    elif value <= 40:
        emoji = "ok"
    elif value <= 60:
        emoji = "good"
    elif value <= 80:
        emoji = "great"
    else:
        emoji = "fire"

    await message.reply_text(f"? {text}\n\nAnswer: {value}% {emoji}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("percent", percent))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_percent_message))
    print("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
