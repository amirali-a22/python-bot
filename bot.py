import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BASE_DIR = os.path.dirname(__file__)

def read_secrets() -> dict:
    filename = os.path.join(BASE_DIR, 'secrets.json') 
    try:
        with open(filename, mode='r') as f:
            f = f.read()
            return json.loads(f)
    except FileNotFoundError:
        return {}
    
secrets = read_secrets()
TOKEN = secrets.get("TOKEN")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

if __name__ == "__main__":
    print('bot polling')
    app.run_polling()