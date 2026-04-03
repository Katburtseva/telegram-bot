import random
import re
import threading
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

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
    return "█" * filled + "░" * empty


def get_emoji_by_value(value: int) -> str:
    if value == 100:
        return "🔥"
    if value >= 90:
        return "💯"
    if value >= 75:
        return "😋"
    if value >= 60:
        return "😏"
    if value >= 45:
        return "🤔"
    if value >= 30:
        return "😅"
    if value >= 15:
        return "😬"
    if value > 0:
        return "❄️"
    return "🚫"


def get_comment_by_value(value: int) -> str:
    if value == 100:
        return "Это ты на все 100! Без сомнений"
    if value >= 90:
        return "Почти идеальное совпадение!"
    if value >= 75:
        return "Очень даже да, не отпирайся"
    if value >= 60:
        return "Больше да, чем нет"
    if value >= 45:
        return "Ну... примерно так и есть"
    if value >= 30:
        return "Скорее нет, но искра есть!"
    if value >= 15:
        return "Почти не про тебя, почти..."
    if value > 0:
        return "Ну совсем чуть-чуть"
    return "Категорически не ты!"


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
        f"{emoji} <i>{comment}</i>"
    )


def build_choice_options(text: str) -> tuple[str, str] | None:
    options = re.split(r"\s+или\s+", text, maxsplit=1, flags=re.IGNORECASE)
    if len(options) != 2:
        return None

    option1 = options[0].strip(" \"'")
    option2 = options[1].strip(" \"'")
    if not option1 or not option2:
        return None

    option1_words = option1.split()
    option2_words = option2.split()

    if len(option1_words) > 1 and len(option2_words) == 1:
        option2 = " ".join(option1_words[:-1] + [option2_words[0]])

    return option1, option2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ <b>Привет!</b> ✨\n"
        "\n"
        "Напиши любое слово или фразу,\n"
        "и я скажу, на сколько процентов это про тебя.\n"
        "\n"
        "Если напишешь что-то вроде <b>чай или кофе</b>,\n"
        "я выберу один из двух вариантов.\n"
        "\n"
        "Ещё можно просто написать <b>выбор</b>, и я покажу пример.",
        parse_mode="HTML",
    )


async def random_percent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text.strip()
    lower_text = text.lower()

    if lower_text == "выбор":
        await message.reply_text(
            "Выбор из двух\n"
            "\n"
            "Напиши, например:\n"
            "<b>чай или кофе</b>",
            parse_mode="HTML",
        )
        return

    choice_options = build_choice_options(text)
    if choice_options:
        chosen = random.choice(choice_options)
        await message.reply_text(chosen)
        return

    value = random.randint(0, 100)
    await message.reply_text(format_result(text, value), parse_mode="HTML")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return

    choice_options = build_choice_options(query)
    if choice_options:
        chosen = random.choice(choice_options)
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Нажми, чтобы узнать выбор",
                description=query,
                input_message_content=InputTextMessageContent(chosen),
            )
        ]
        await update.inline_query.answer(results, cache_time=0)
        return

    value = random.randint(0, 100)
    result_text = format_result(query, value)

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Нажми, чтобы узнать результат",
            description="Нажми, чтобы узнать результат!",
            input_message_content=InputTextMessageContent(
                result_text,
                parse_mode="HTML",
            ),
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
