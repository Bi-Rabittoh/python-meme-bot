from PIL import Image
from Api import get_random_image, rating_normal, rating_lewd
from Effects import img_to_bio, tt_bt_effect, bt_effect, splash_effect, wot_effect, text_effect
from Constants import get_localized_string as l

from dotenv import load_dotenv
load_dotenv()
import os, logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from io import BytesIO

from telegram.error import TelegramError
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, PicklePersistence
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

lang = 'us'

def _get_args(context):
    
    logging.info(context.args)
    return ' '.join(context.args)

def _get_message_content(message):
    
    image = None
    if len(message.photo) > 0:
        image = message.photo[-1].get_file()
        image = Image.open(BytesIO(image.download_as_bytearray()))
    
    content = ""
    if message.text is not None:
        content = message.text.strip()
    elif message.caption is not None:
        content = message.caption.strip()
        
    lines = content.split("\n")
    r = lines[0].split(" ")
    
    try:
        if r[0][0] == '/':
            r.pop(0)
    except IndexError:
        pass
        
    lines[0] = " ".join(r)
    content = "\n".join(lines)
    
    return image, content, _get_author(message)

def _get_reply(message, fallback=""):
    
    if message is None:
        return None, fallback, None
    
    image, content, author = _get_message_content(message)
    
    return image, content, author

def _get_lewd(context):
    
    try:
        return context.chat_data["lewd"]
    except KeyError:
        return False

def _get_image(context, tag="", bio=True):
    
    if context is not None:
        if _get_lewd(context):
            image, url = get_random_image(rating_lewd, tag)
        else:
            image, url = get_random_image(rating_normal, tag)
    
    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("sauce", lang), url=url)]])
    
    if bio:
        return image, markup
    return image, markup

def _get_all(update, check_fn, context):
    
    image_reply, text_reply, author_reply = _get_reply(update.message.reply_to_message)
    image_content, text_content, author_content = _get_message_content(update.message)
    
    info_struct = {
        "reply": {
            "author": author_reply,
            "text": text_reply,
            "image": image_reply
        },
        "content": {
            "author": author_content,
            "text": text_content,
            "image": image_content
        }
    }
        
    logging.info(f"User {update.message.from_user.full_name} (@{update.message.from_user.username}) typed: {str(update.message.text)}")
    
    content = check_fn(info_struct)
    
    if content is None:
        return None, None, None

    markup = ""
    image = None
    
    if image_reply is not None:
        image = image_reply
    
    if image_content is not None:
        image = image_content
    
    if image is None:
        image, markup = _get_image(context, bio=False)
    
    return content, image, markup

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
    
    try:
        tag = " " + context.args[0]
    except IndexError:
        tag = ""

    image, markup = _get_image(context, tag)
    update.message.reply_photo(photo=img_to_bio(image), parse_mode="markdown", reply_markup=markup)

def raw(update: Update, context: CallbackContext):
    
    tag = ""
    try:
        tag += " " + context.args[0]
        tag += " " + context.args[1]
    except IndexError:
        pass
    
    image, url = get_random_image("", tag)
    
    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")
    
    image = _img_to_bio(image)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("sauce", lang), url=url)]])
    
    update.message.reply_photo(photo=image, parse_mode="markdown", reply_markup=markup)

def pilu(update: Update, context: CallbackContext):
    
    logging.warning(f"User {update.message.from_user.username} requested an explicit pic.")
    try:
        tag = " " + context.args[0]
    except IndexError:
        tag = ""
    image, url = get_random_image("rating:e" + tag)
    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")
        return
    
    image = _img_to_bio(image)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("sauce", lang), url=url)]])
    
    update.message.reply_photo(photo=image, parse_mode="markdown", reply_markup=markup)

def _format_author(user):
    
    if user.username is not None:
        return user.full_name + f" ({user.username})"
    return user.full_name

def _get_author(message):
    
    if message.forward_from is not None:
        return _format_author(message.forward_from)
    
    if message.forward_sender_name is not None:
        return message.forward_sender_name
    
    if message.forward_from_chat is not None:
        return message.forward_from_chat.title + ("" if message.forward_from_chat.username is None else f" ({message.forward_from_chat.username})")
    
    return _format_author(message.from_user)

def tt_check(info):
    
    reply = info['reply']['text']
    content = info['content']['text']
    
    input_text = f"{reply} {content}".replace("\n", " ")
    
    if input_text.strip() == "":
        return None

    return input_text

def ttbt_check(info):
    
    reply = info['reply']['text'].strip()
    content = info['content']['text'].strip()
    
    if len(content.split("\n")) > 1:
        input_text = content
    else:
        input_text = f"{reply}\n{content}"
    
    if input_text.strip() == "":
        return None

    return input_text

def splash_check(info):
    
    reply = info['reply']['text']
    content = info['content']['text']
    
    if content.strip() == "":
        author = info['reply']['author']
        input_text = f"{author}\n{reply}"
    else:
        author = info['content']['author']
        input_text = f"{author}\n{content}"

    if len(input_text.strip().split("\n")) < 2:
        return None

    return input_text

def wot_check(info):
    
    reply = info['reply']['text']
    content = info['content']['text']
    
    input_text = f"{reply}\n{content}"

    if input_text.strip() == "":
        return None

    return input_text

def ttbt(update: Update, context: CallbackContext):
    
    content, image, markup = _get_all(update, ttbt_check, context)
    
    if image is None:
        update.message.reply_text(l("no_caption", lang))
        return
    
    image = tt_bt_effect(content, image)

    if image is None:
        update.message.reply_text(l("failed_effect", lang))

    update.message.reply_photo(photo=image, reply_markup=markup)


def tt(update: Update, context: CallbackContext):
    
    content, image, markup = _get_all(update, tt_check, context)
    
    if image is None:
        update.message.reply_text(l("no_caption", lang))
        return
    
    image = tt_bt_effect(content, image)

    if image is None:
        update.message.reply_text(l("failed_effect", lang))

    update.message.reply_photo(photo=image, reply_markup=markup)
    
def bt(update: Update, context: CallbackContext):
    
    content, image, markup = _get_all(update, tt_check, context)
    
    if image is None:
        update.message.reply_text(l("no_caption", lang))
        return

    image = bt_effect(content, image)

    if image is None:
        update.message.reply_text(l("failed_effect", lang))

    update.message.reply_photo(photo=image, reply_markup=markup)

def splash(update: Update, context: CallbackContext):
    
    content, image, markup = _get_all(update, splash_check, context)
    
    if image is None:
        update.message.reply_text(l("no_caption", lang))
        return
    
    image = splash_effect(content, image)

    if image is None:
        update.message.reply_text(l("failed_effect", lang))
    
    update.message.reply_photo(photo=image, reply_markup=markup)
    
def wot(update: Update, context: CallbackContext):
    
    content, image, markup = _get_all(update, wot_check, context)
    
    if image is None:
        update.message.reply_text(l("no_caption", lang))
        return
    
    image = wot_effect(content, image)

    if image is None:
        update.message.reply_text(l("failed_effect", lang))
    
    update.message.reply_photo(photo=image, reply_markup=markup)
    
def text(update: Update, context: CallbackContext):
    
    content, image, markup = _get_all(update, wot_check, context)
    
    if image is None:
        update.message.reply_text(l("no_caption", lang))
        return
    
    image = text_effect(content, image)

    if image is None:
        update.message.reply_text(l("failed_effect", lang))
    
    update.message.reply_photo(photo=image, reply_markup=markup)

def caps(update: Update, context: CallbackContext):
    
    _, reply, _ = _get_reply(update.message.reply_to_message, _get_args(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply.upper())
    
def unknown(update: Update, context: CallbackContext):
    logging.info(f"User {update.message.from_user.full_name} sent {update.message.text_markdown_v2} and I don't know what that means.")
    
def error_callback(update: Update, context: CallbackContext):
    try:
        raise context.error
    except TelegramError:
        logging.error("TelegramError!!")
        context.bot.send_message(chat_id=update.effective_chat.id, text=l('error', lang))
        
def _add_effect_handler(dispatcher, command: str, callback):
    dispatcher.add_handler(CommandHandler(command, callback))
    dispatcher.add_handler(MessageHandler(Filters.caption(update=[f"/{command}"]), callback))
    
def main():
    
    updater = Updater(token=os.getenv("token"),
                      persistence=PicklePersistence(filename='bot-data.pkl',
                                                    store_bot_data=False,
                                                    store_callback_data=False,
                                                    store_user_data=False))
    
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_callback)
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('lewd', set_lewd))
    dispatcher.add_handler(CommandHandler('caps', caps))
    dispatcher.add_handler(CommandHandler('pic', pic))
    dispatcher.add_handler(CommandHandler('raw', raw))
    dispatcher.add_handler(CommandHandler('pilu', pilu))
    
    _add_effect_handler(dispatcher, 'ttbt', ttbt)
    _add_effect_handler(dispatcher, 'tt', tt)
    _add_effect_handler(dispatcher, 'bt', bt)
    _add_effect_handler(dispatcher, 'splash', splash)
    _add_effect_handler(dispatcher, 'wot', wot)
    _add_effect_handler(dispatcher, 'text', text)
    
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()

if __name__ ==  "__main__":
    main()
