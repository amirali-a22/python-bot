import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BASE_DIR = os.path.dirname(__file__)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

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

# app = ApplicationBuilder().token(TOKEN).build()

# app.add_handler(CommandHandler("hello", hello))

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("hello", hello))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    print('bot polling')
    main()