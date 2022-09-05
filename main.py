from PIL import Image
from Api import get_random_image, rating_normal, rating_lewd
from Effects import tt_bt_effect
import Constants as C
from Constants import get_localized_string as l

from dotenv import load_dotenv
load_dotenv()
import os, logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from io import BytesIO

from telegram.error import TelegramError, BadRequest
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update

lang = 'us'

def _get_args(context):
    logging.info(context.args)
    return ' '.join(context.args)

def _img_to_bio(image):
    bio = BytesIO()
    #bio.name = 'image.jpeg'
    
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio

def _ttbt_general(context, text):
    if text.strip() == "":
        return None, l("no_caption", lang)
    
    image, url = _get_image(context, bio=False)
    image = tt_bt_effect(text, image)
    return _img_to_bio(image), url

def _get_reply(input, fallback=""):
    if input is None:
        return fallback
    return input.text

def _get_lewd(context):
    try:
        return context.chat_data["lewd"]
    except KeyError:
        return False

def _get_image(context, bio=True):
    if context is not None:
        if _get_lewd(context):
            image, url = get_random_image(rating_lewd)
        else:
            image, url = get_random_image(rating_normal)
    
    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")
    
    url = l("sauce", lang).format(url)
    if bio:
        return _img_to_bio(image), url
    return image, url
    

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=l("welcome", lang))

def set_lewd(update: Update, context: CallbackContext):
    try:
        output = False if context.chat_data["lewd"] else True
    except KeyError:
        output = True
        
    context.chat_data['lewd'] = output
    message = l("lewd_toggle", lang).format(l("enabled", lang) if output else l("disabled", lang))
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def pic(update: Update, context: CallbackContext):
    image, url = _get_image(context)
    update.message.reply_photo(photo=image, caption=url, parse_mode="markdown")

def pilu(update: Update, context: CallbackContext):
    logging.warning(f"User {update.message.from_user.username} requested an explicit pic.")
    try:
        tag = " " + context.args[0]
    except IndexError:
        tag = ""
    image, url = get_random_image("e" + tag)
    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")
        return
    url = l("sauce", lang).format(url)
    image = _img_to_bio(image)
    update.message.reply_photo(photo=image, caption=url, parse_mode="markdown")

def tt(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message)
    content = _get_args(context)
    input_text = f"{reply} {content}".replace("\n", " ")
    
    image, url = _ttbt_general(context, input_text)
    
    if image is None:
        update.message.reply_text(url)
        return
    update.message.reply_photo(photo=image, caption=url, parse_mode="markdown")

def bt(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message)
    content = _get_args(context)
    input_text = f"{reply} {content}".replace("\n", " ")
    
    image, url =_ttbt_general(context, " \n" + input_text)
    
    if image is None:
        update.message.reply_text(url)
        return
    update.message.reply_photo(photo=image, caption=url, parse_mode="markdown")

def ttbt(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message)
    content = _get_args(context)
    input_text = f"{reply}\n{content}"
    
    image, url =_ttbt_general(context, input_text)
    
    if image is None:
        update.message.reply_text(url)
        return
    update.message.reply_photo(photo=image, caption=url, parse_mode="markdown")
    
def caps(update: Update, context: CallbackContext):
    reply = _get_reply(update.message.reply_to_message, _get_args(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply.upper())
    
def unknown(update: Update, context: CallbackContext):
    logging.info(f"User {update.message.from_user.username} sent {_get_args(context)}")
    context.bot.reply_text(text=l("unknown", lang))
    
def error_callback(update: Update, context: CallbackContext):
    try:
        raise context.error
    #except BadRequest:
    #    logging.error("BadRequest!!")
    except TelegramError:
        logging.error("TelegramError!!")
        context.bot.send_message(chat_id=update.effective_chat.id, text=l('error', lang))
def main():
    
    updater = Updater(token=os.getenv("token"))
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_callback)
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('lewd', set_lewd))
    dispatcher.add_handler(CommandHandler('caps', caps))
    dispatcher.add_handler(CommandHandler('pic', pic))
    dispatcher.add_handler(CommandHandler('pilu', pilu))
    dispatcher.add_handler(CommandHandler('ttbt', ttbt))
    dispatcher.add_handler(CommandHandler('tt', tt))
    dispatcher.add_handler(CommandHandler('bt', bt))
    
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()

if __name__ ==  "__main__":
    main()
