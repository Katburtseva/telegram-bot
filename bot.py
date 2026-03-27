import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, InlineQueryHandler, filters, ContextTypes
import uuid

BOT_TOKEN = "8372379665:AAFjHFztodzZTBz8gBVSrhECQmx9CTjoHeI"


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass


def run_health_server():
    server = HTTPServer(("0.0.0.0", 10000), HealthHandler)
    server.serve_forever()


def make_progress_bar(value: int, length: int = 10) -> str:
    filled = round(value / 100 * length)
    empty = length - filled
    return "▓" * filled + "░" * empty


def get_emoji_by_value(value: int) -> str:
    if value == 100:
        return "🔥"
    elif value >= 90:
        return "💯"
    elif value >= 75:
        return "😎"
    elif value >= 60:
        return "😏"
    elif value >= 45:
        return "🤔"
    elif value >= 30:
        return "😅"
    elif value >= 15:
        return "😬"
    elif value > 0:
        return "❄️"
    else:
        return "🚫"


def get_comment_by_value(value: int) -> str:
    if value == 100:
        return "Это ты на все 100! Без сомнений 👑"
    elif value >= 90:
        return "Почти идеальное совпадение!"
    elif value >= 75:
        return "Очень даже да, не отпирайся 😄"
    elif value >= 60:
        return "Больше да, чем нет~"
    elif value >= 45:
        return "Ну... примерно так и есть 🤷"
    elif value >= 30:
        return "Скорее нет, но искра есть!"
    elif value >= 15:
        return "Почти не про тебя, почти..."
    elif value > 0:
        return "Ну совсем чуть-чуть 🌚"
    else:
        return "Категорически не ты! 😤"


def format_result(text: str, value: int) -> str:
    bar = make_progress_bar(value)
    emoji = get_emoji_by_value(value)
    comment = get_comment_by_value(value)

    return (
        f"<b>{text}</b>\n"
        f"\n"
        f"┌─────────────────────┐\n"
        f"│  {bar}  {value:>3}%  │\n"
        f"└─────────────────────┘\n"
        f"\n"
        f"💬 <i>{comment}</i>"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ <b>Привет!</b> ✨\n"
        "\n"
        "Напиши любое слово или фразу —\n"
        "и я скажу, на сколько процентов это про тебя!\n"
        "\n"
        "📌 Также работает в инлайн-режиме:\n"
        "введи <code>@имя_бота текст</code> в любом чате\n"
        "\n"
        "🎲 Попробуй прямо сейчас!",
        parse_mode="HTML"
    )


async def random_percent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text
    value = random.randint(0, 100)
    result = format_result(text, value)
    await message.reply_text(result, parse_mode="HTML")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return

    value = random.randint(0, 100)
    result_text = format_result(query, value)
    emoji = get_emoji_by_value(value)

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"{emoji} {query}",
            description=f"Результат: {value}% — нажми чтобы поделиться!",
            input_message_content=InputTextMessageContent(
                result_text,
                parse_mode="HTML"
            )
        )
    ]
    await update.inline_query.answer(results, cache_time=0)


def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_percent_message))
    print("Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
