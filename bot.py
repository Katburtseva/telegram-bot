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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!\n\n"
        "Напиши любое слово или фразу, и я скажу, "
        "на сколько процентов это про тебя!\n\n"
    )

async def random_percent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text
    value = random.randint(0, 100)
    await message.reply_text(f"Вопрос: {text}\n\nОтвет: {value}%")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return

    value = random.randint(0, 100)
    result_text = f"Вопрос: {query}\n\nОтвет: {value}%"

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=query,
            description="Нажми чтобы узнать результат",
            input_message_content=InputTextMessageContent(result_text)
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
