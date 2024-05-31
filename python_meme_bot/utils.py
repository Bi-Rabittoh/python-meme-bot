from io import BytesIO
import logging

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup, Message, Update, User
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from PIL import Image

from python_meme_bot.api import get_random_image

def format_author(user: User):
    if user.username is not None:
        return user.full_name + f" ({user.username})"
    return user.full_name

def format_chat(chat: Chat):
    return chat.title + ("" if chat.username is None else f" ({chat.username})")

def _get_lewd(context: ContextTypes.DEFAULT_TYPE):
    try:
        return context.chat_data["lewd"]
    except KeyError:
        return False
    
def _get_author(message: Message):
    origin = message.forward_origin
    
    if origin is None: # message was not forwarded
        return format_author(message.from_user)
    
    try:
        return format_author(origin['sender_user']) # MessageOriginUser
    except KeyError:
        pass
    
    try:
        return origin['sender_user_name'] # MessageOriginHiddenUser
    except KeyError:
        pass
    
    try:
        return format_chat(origin['sender_chat']) # MessageOriginChat
    except KeyError:
        pass
    try:
        return format_chat(origin['chat']) # MessageOriginChannel
    except KeyError:
        pass
    
    logging.warn("Message was forwarded but I couldn't detect the original author.")
    return format_author(message.from_user)
    
async def get_message_content(message: Message, fallback: str = ""):
    if message is None:
        return None, fallback, None
    
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

def get_image(context: ContextTypes.DEFAULT_TYPE):
    if context is not None:
        image, url = get_random_image(_get_lewd(context))

    if image is None:
        logging.warning("Getting Image failed")
        raise TelegramError("bad image")

    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Sauce 🍝", url=url)]])
    return image, markup

async def get_all(update: Update, check_fn, context: ContextTypes.DEFAULT_TYPE):
    image_reply, text_reply, author_reply = await get_message_content(update.message.reply_to_message)
    image_content, text_content, author_content = await get_message_content(update.message)

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
        image, markup = get_image(context)

    return content, image, markup
