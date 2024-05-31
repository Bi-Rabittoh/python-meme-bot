from functools import partial
import os, logging


from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, \
    PicklePersistence, filters, PersistenceInput, ContextTypes
from telegram.error import TelegramError

from .utils import get_all, get_image, get_message_content
from .effects.functions import img_to_bio
from .slot import spin, autospin, bet, cash
from .effects import effectsDict
from .localization import get_localized_string as l, format_lang, get_lang, langs, lang_markup

async def effect_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, effect_name: str):
    try:
        effect_check, effect_fn = effectsDict[effect_name]
    except KeyError:
        raise TelegramError("effect not supported: " + effect_name)
    
    content, image, markup = await get_all(update, effect_check, context)

    if image is None:
        await update.message.reply_text(l("no_caption", context))
        return

    image = effect_fn(content, image)

    if image is None:
        await update.message.reply_text(l("failed_effect", context))
        return

    await update.message.reply_photo(photo=image, reply_markup=markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(l("welcome", context))


async def lewd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        output = False if context.chat_data["lewd"] else True
    except KeyError:
        output = True

    context.chat_data['lewd'] = output
    message = l("lewd_toggle", context).format(l("enabled", context) if output else l("disabled", context))
    await update.message.reply_text(message)


async def pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image, markup = get_image(context)
    await update.message.reply_photo(photo=img_to_bio(image), parse_mode="markdown", reply_markup=markup)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _, reply, _ = await get_message_content(update.message.reply_to_message, ' '.join(context.args))
    await update.message.reply_text(reply.upper())


async def _set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    context.chat_data["lang"] = lang
    response = l("language_set", context).format(format_lang(lang))
    await update.message.reply_text(response)


async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        selected = str(context.args[0])
    except IndexError:
        selected = None

    if selected is None:
        lang = format_lang(get_lang(context))
        choices = ", ".join(langs) + "."
        text = l("current_language", context).format(lang, choices)
        return await update.message.reply_text(text,reply_markup=lang_markup)

    if selected not in langs:
        return await update.message.reply_text(text=l("invalid_language", context))

    return await _set_lang(update, context, selected)


def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"User {update.message.from_user.full_name} sent {update.message.text_markdown_v2} and I don't know what that means.")


async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        raise context.error
    except Exception as e:
        logging.error(str(e))
        await update.message.reply_text(l('error', context))


def _add_effect_handler(application: ApplicationBuilder, command: str):
    callback = partial(effect_handler, effect_name=command)

    application.add_handler(CommandHandler(command, callback))
    application.add_handler(MessageHandler(filters.Caption([f"/{command}"]), callback))

async def keyboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = os.getenv("token")
    pers = PersistenceInput(bot_data=False, callback_data=False)
    persistence = PicklePersistence(filepath='bot-data.pkl', store_data=pers)

    application = ApplicationBuilder().token(token).persistence(persistence).build()

    application.add_error_handler(error_callback)
    application.add_handler(CallbackQueryHandler(callback=keyboard_handler))

    # commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('lang', lang))
    application.add_handler(CommandHandler('lewd', lewd))
    application.add_handler(CommandHandler('caps', caps))
    application.add_handler(CommandHandler('pic', pic))

    # effects
    _add_effect_handler(application, 'ttbt')
    _add_effect_handler(application, 'tt')
    _add_effect_handler(application, 'bt')
    _add_effect_handler(application, 'splash')
    _add_effect_handler(application, 'wot')
    _add_effect_handler(application, 'text')

    # games
    application.add_handler(CommandHandler('spin', spin))
    application.add_handler(CommandHandler('bet', bet))
    application.add_handler(CommandHandler('cash', cash))

    # fallback
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()


if __name__ == "__main__":
    main()
