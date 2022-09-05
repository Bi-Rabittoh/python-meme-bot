from PIL import Image
from Api import get_random_image
from Effects import tt_bt

from dotenv import load_dotenv
load_dotenv()
import os, logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from io import BytesIO

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update

sauce_str = "[Sauce 🍝]({})"

def _ttbt_general(text):
    image, url = get_random_image()
    image = tt_bt(text, image)
    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio, sauce_str.format(url)

def _get_reply(input, fallback=""):
    if input is None:
        return fallback
    return input.text

def _get_image():
    image, url = get_random_image()
    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio, sauce_str.format(url)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to PILuAnimeBot!")

def pic(update: Update, context: CallbackContext):
    image, url = _get_image()
    
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=url, parse_mode="markdown")

def tt(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message)
    content = ' '.join(context.args)
    input_text = f"{reply} {content}".replace("\n", " ")
    
    image, url = _ttbt_general(input_text)
    context.bot.send_photo(update.effective_chat.id, photo=image, caption=url, parse_mode="markdown")

def bt(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message)
    content = ' '.join(context.args)
    input_text = f"{reply} {content}".replace("\n", " ")
    
    image, url =_ttbt_general(" \n" + input_text)
    context.bot.send_photo(update.effective_chat.id, photo=image, caption=url, parse_mode="markdown")

def ttbt(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message)
    content = ' '.join(context.args)
    input_text = f"{reply}\n{content}"
    
    image, url =_ttbt_general(input_text)
    context.bot.send_photo(update.effective_chat.id, photo=image, caption=url, parse_mode="markdown")
    
def caps(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message, ' '.join(context.args))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply.upper())
    
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    
    updater = Updater(token=os.getenv("token"))
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('caps', caps))
    dispatcher.add_handler(CommandHandler('pic', pic))
    dispatcher.add_handler(CommandHandler('ttbt', ttbt))
    dispatcher.add_handler(CommandHandler('tt', tt))
    dispatcher.add_handler(CommandHandler('bt', bt))
    
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    
    updater.start_polling()
    updater.idle()

if __name__ ==  "__main__":
    main()
