from PIL import Image
from Api import get_random_image
from Effects import img_to_bio, tt_bt_effect, bt_effect, splash_effect, wot_effect, text_effect
from Constants import get_localized_string as l, format_author, format_lang, langs, get_lang, lang_markup
from Slot import spin, autospin, bet, cash

from dotenv import load_dotenv
load_dotenv()
import os, logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from io import BytesIO

from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, Updater, CallbackContext, CallbackQueryHandler, CommandHandler, MessageHandler, PicklePersistence, filters, PersistenceInput
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

async def _get_message_content(message):
    
    image = None
    if len(message.photo) > 0:
        p = message.photo[-1]
        i = await p.get_file()
        d = await i.download_as_bytearray()
        image = Image.open(BytesIO(d))
    
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

async def _get_reply(message, fallback=""):
    
    if message is None:
        return None, fallback, None
    
    image, content, author = await _get_message_content(message)
    
    return image, content, author

def _get_lewd(context):
    
    try:
        return context.chat_data["lewd"]
    except KeyError:
        return False

def _get_image(context):
    
    if context is not None:
        image, url = get_random_image(_get_lewd(context))
    
    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("sauce", context), url=url)]])

    return image, markup

async def _get_all(update, check_fn, context):
    
    image_reply, text_reply, author_reply = await _get_reply(update.message.reply_to_message)
    image_content, text_content, author_content = await _get_message_content(update.message)
    
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
        
    logging.info(f"User {update.message.from_user.full_name}{f' (@{update.message.from_user.username})' if update.message.from_user.username is not None else ''} typed: {str(update.message.text)}")
    
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
        image, markup = _get_image(context)
    
    return content, image, markup

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=l("welcome", context))

async def set_lewd(update: Update, context: CallbackContext):
    
    try:
        output = False if context.chat_data["lewd"] else True
    except KeyError:
        output = True
        
    context.chat_data['lewd'] = output
    message = l("lewd_toggle", context).format(l("enabled", context) if output else l("disabled", context))
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def pic(update: Update, context: CallbackContext):
    
    image, markup = _get_image(context)
    return await update.message.reply_photo(photo=img_to_bio(image), parse_mode="markdown", reply_markup=markup)

def _get_author(message):
    
    if message.forward_from is not None:
        return format_author(message.forward_from)
    
    if message.forward_sender_name is not None:
        return message.forward_sender_name
    
    if message.forward_from_chat is not None:
        return message.forward_from_chat.title + ("" if message.forward_from_chat.username is None else f" ({message.forward_from_chat.username})")
    
    return format_author(message.from_user)

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

async def ttbt(update: Update, context: CallbackContext):
    
    content, image, markup = await _get_all(update, ttbt_check, context)
    
    if image is None:
        return await update.message.reply_text(l("no_caption", context))
    
    image = tt_bt_effect(content, image)

    if image is None:
        return await update.message.reply_text(l("failed_effect", context))

    return await update.message.reply_photo(photo=image, reply_markup=markup)


async def tt(update: Update, context: CallbackContext):
    
    content, image, markup = await _get_all(update, tt_check, context)
    
    if image is None:
        return await update.message.reply_text(l("no_caption", context))
    
    image = tt_bt_effect(content, image)

    if image is None:
        return await update.message.reply_text(l("failed_effect", context))

    return await update.message.reply_photo(photo=image, reply_markup=markup)
    
async def bt(update: Update, context: CallbackContext):
    
    content, image, markup = await _get_all(update, tt_check, context)
    
    if image is None:
        return await update.message.reply_text(l("no_caption", context))

    image = bt_effect(content, image)

    if image is None:
        return await update.message.reply_text(l("failed_effect", context))

    return await update.message.reply_photo(photo=image, reply_markup=markup)

async def splash(update: Update, context: CallbackContext):
    
    content, image, markup = await _get_all(update, splash_check, context)
    
    if image is None:
        return await update.message.reply_text(l("no_caption", context))
    
    image = splash_effect(content, image)

    if image is None:
        return await update.message.reply_text(l("failed_effect", context))
    
    return await update.message.reply_photo(photo=image, reply_markup=markup)
    
async def wot(update: Update, context: CallbackContext):
    
    content, image, markup = await _get_all(update, wot_check, context)
    
    if image is None:
        return await update.message.reply_text(l("no_caption", context))
    
    image = wot_effect(content, image)

    if image is None:
        await update.message.reply_text(l("failed_effect", context))
    
    await update.message.reply_photo(photo=image, reply_markup=markup)
    
async def text(update: Update, context: CallbackContext):
    
    content, image, markup = await _get_all(update, wot_check, context)
    
    if image is None:
        await update.message.reply_text(l("no_caption", context))
        return
    
    image = text_effect(content, image)

    if image is None:
        await update.message.reply_text(l("failed_effect", context))
    
    await update.message.reply_photo(photo=image, reply_markup=markup)

async def caps(update: Update, context: CallbackContext):
    
    _, reply, _ = await _get_reply(update.message.reply_to_message, ' '.join(context.args))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply.upper())

async def _set_lang(update: Update, context: CallbackContext, lang: str):
    context.chat_data["lang"] = lang
    await context.bot.send_message(chat_id=update.effective_chat.id, text=l("language_set", context).format(format_lang(lang)))

async def lang(update: Update, context: CallbackContext):
    try:
        selected = str(context.args[0])
    except IndexError:
        selected = None
    
    if selected is None:
        lang = format_lang(get_lang(context))
        choices = ", ".join(langs) + "."
        return await update.message.reply_text(text=l("current_language", context).format(lang, choices), reply_markup=lang_markup)
    
    if selected not in langs:
        return await update.message.reply_text(text=l("invalid_language", context))
    
    return await _set_lang(update, context, selected)
    
def unknown(update: Update, context: CallbackContext):
    logging.info(f"User {update.message.from_user.full_name} sent {update.message.text_markdown_v2} and I don't know what that means.")
    
async def error_callback(update: Update, context: CallbackContext):
    try:
        raise context.error
    except TelegramError as e:
        logging.error("TelegramError! " + str(e))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=l('error', context))
        
def _add_effect_handler(application: ApplicationBuilder, command: str, callback):
    application.add_handler(CommandHandler(command, callback))
    application.add_handler(MessageHandler(filters.Caption([f"/{command}"]), callback))

async def keyboard_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    if data.startswith("reroll"):
        amount = int(data.split(" ")[1])
        
        if amount <= 1:
            return await spin(update, context)
        return await autospin(context, update.effective_chat.id, amount)
    
    match data:
        case "none":
            return query.answer(l("none_callback", context))
        case "set_lang_en":
            lang = "en"
            await _set_lang(update, context, lang)
            return await query.answer(l("language_set", context).format(format_lang(lang)))
        case "set_lang_it":
            lang = "it"
            await _set_lang(update, context, lang)
            return await query.answer(l("language_set", context).format(format_lang(lang)))
        case other:
            logging.error(f"unknown callback: {data}")
    
    return await query.answer()

def main():
    
    pers = PersistenceInput(bot_data = False, callback_data = False)
    
    application = ApplicationBuilder()
    application.token(os.getenv("token"))
    application.persistence(PicklePersistence(filepath='bot-data.pkl', store_data=pers))
    
    application = application.build()

    
    application.add_error_handler(error_callback)
    application.add_handler(CallbackQueryHandler(callback=keyboard_handler))
    
    # commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('lang', lang))
    application.add_handler(CommandHandler('lewd', set_lewd))
    application.add_handler(CommandHandler('caps', caps))
    application.add_handler(CommandHandler('pic', pic))
    
    # effects
    _add_effect_handler(application, 'ttbt', ttbt)
    _add_effect_handler(application, 'tt', tt)
    _add_effect_handler(application, 'bt', bt)
    _add_effect_handler(application, 'splash', splash)
    _add_effect_handler(application, 'wot', wot)
    _add_effect_handler(application, 'text', text)
    
    # games
    application.add_handler(CommandHandler('spin', spin))
    application.add_handler(CommandHandler('bet', bet))
    application.add_handler(CommandHandler('cash', cash))
    
    # fallback
    application.add_handler(MessageHandler(filters.Command(), unknown))
    application.run_polling()

if __name__ ==  "__main__":
    main()
