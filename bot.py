import os
import json
import sys
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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
# def error(update: Update, context: CallbackContext):
#     """Log Errors caused by Updates."""
#     sys.stderr.write(f"ERROR: '{context.error}' caused by '{update}'")
#     pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
        InlineKeyboardButton("wallet", callback_data='1'),
        InlineKeyboardButton("buy config", callback_data='2')
        ], 
    [InlineKeyboardButton("test free config", callback_data='3')],
    [
        InlineKeyboardButton("invite link", callback_data='4'),
        InlineKeyboardButton("my services", callback_data='5'),
     ],
    [
        InlineKeyboardButton("guide", callback_data='6'),
        InlineKeyboardButton("support", callback_data='7'),
     ],
    [InlineKeyboardButton("roles", callback_data='8')],

    ]

    # creating a reply markup of inline keyboard options
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.inlinekeyboardmarkup.html
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.message.id
    # sending the message to the current chat id
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message.reply_text
    await update.message.reply_text(f'Hi {update.effective_user.first_name}')
    await update.message.reply_text('Please choose:', reply_markup=reply_markup, reply_to_message_id=chat_id)


async def button(update, context):
    """
    callback method handling button press
    """
    # getting the callback query
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html
    query: CallbackQuery = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html#telegram.CallbackQuery.answer
    await query.answer()

    # editing message sent by the bot
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html#telegram.CallbackQuery.edit_message_text
    if query.data == '1':
        # await query.edit_message_text(text=f"hey, fuck you: {query.data}")
        await query.edit_message_text(text=f"hey, fuck you: {query.data}")
    else:
        await query.message.reply_text(text=f"Selected option: {query.data}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    # application.add_error_handler(error)  # error handling
    application.add_handler(CallbackQueryHandler(button))  
    # application.add_handler(CallbackQueryHandler(test, pattern='^5_test'))  

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    print('bot polling')
    main()