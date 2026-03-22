import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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
    message = update.message
    text = message.text
    bot_username = context.bot.username

    # В группах реагируем только на упоминание @бота
    if message.chat.type in ["group", "supergroup"]:
        mention = f"@{bot_username}"
        if mention.lower() not in text.lower():
            return
        # Убираем упоминание из текста
        text = text.replace(mention, "").replace(mention.lower(), "").strip()
        if not text:
            text = "это"

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

    await message.reply_text(
        f"❓ «{text}»\n\nОтвет: {value}% {emoji}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("percent", percent))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_percent_message))
    print("✅ Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
```

**Два ключевых изменения в `random_percent_message`:**

1. В группах бот проверяет наличие `@username` в сообщении — если упоминания нет, игнорирует. Если есть — убирает `@username` из текста и отвечает.

2. `run_polling(allowed_updates=Update.ALL_TYPES)` — без этого бот может не получать сообщения из групп.

**Использование в группе:**
```
@твой_бот Насколько я красивый?
