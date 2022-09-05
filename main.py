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
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

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

def _ttbt_general(context, text, image=None):
    if text.strip() == "":
        return None, l("no_caption", lang)
    
    markup = ""
    if image is None:
        image, markup = _get_image(context, bio=False)
    image = tt_bt_effect(text, image)
    return _img_to_bio(image), markup

def _get_reply(input, context, fallback=""):

    if input is None:
        return None, fallback
    
    if input.photo is not None:
        image = input.photo[-1].get_file()
        #image = context.bot.get_file(input.photo[-1].file_id)
        image = Image.open(BytesIO(image.download_as_bytearray()))
    
    if input.caption is not None:
        return image, input.caption
    
    if input.text is not None:
        return image, input.text
    
    return image, fallback

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
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("sauce", lang), url=url)]])
    
    if bio:
        return _img_to_bio(image), markup
    return image, markup
    

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
    image, markup = _get_image(context)
    update.message.reply_photo(photo=image, parse_mode="markdown", reply_markup=markup)

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
    
    image = _img_to_bio(image)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("sauce", lang), url=url)]])
    
    update.message.reply_photo(photo=image, caption=url, parse_mode="markdown", reply_markup=markup)

def tt(update: Update, context: CallbackContext):
    image, reply = _get_reply(update.message.reply_to_message, context)
    content = _get_args(context)
    input_text = f"{reply} {content}".replace("\n", " ")
    
    image, markup = _ttbt_general(context, input_text, image)
    
    if image is None:
        update.message.reply_text(markup)
        return
    update.message.reply_photo(photo=image, parse_mode="markdown", reply_markup=markup)

def bt(update: Update, context: CallbackContext):
    image, reply = _get_reply(update.message.reply_to_message, context)
    content = _get_args(context)
    input_text = f"{reply} {content}".replace("\n", " ")
    
    image, markup =_ttbt_general(context, " \n" + input_text, image)
    
    if image is None:
        update.message.reply_text(markup)
        return
    update.message.reply_photo(photo=image, parse_mode="markdown", reply_markup=markup)

def ttbt(update: Update, context: CallbackContext):
    message = update.message
    
    image, reply = _get_reply(message.reply_to_message, context)
    content = message.text[6:] # /ttbt[space]
    input_text = f"{reply}\n{content}"
    
    image, markup =_ttbt_general(context, input_text, image)
    
    if image is None:
        message.reply_text(markup)
        return
    message.reply_photo(photo=image, parse_mode="markdown", reply_markup=markup)
    
def caps(update: Update, context: CallbackContext):
    _, reply = _get_reply(update.message.reply_to_message, context, _get_args(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply.upper())
    
def unknown(update: Update, context: CallbackContext):
    logging.info(f"User {update.message.from_user.username} sent {update.message.text_markdown_v2} and I don't know what that means.")
    
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
