from telegram import InlineKeyboardMarkup, InlineKeyboardButton, User, Chat
from telegram.ext import CallbackContext
import logging

localization = {
    'en': {
        'name' : "English",
        'emoji' : "🇬🇧",
        'welcome' : "Welcome to PILuAnimeBot!",
        'sauce' : "Sauce 🍝",
        'no_caption' : "No caption detected.",
        'lewd_toggle' : "Lewd content was {} for this chat.",
        'enabled' : "enabled",
        'disabled' : "disabled",
        'unknown' : "Sorry, I didn't understand that command.",
        'error': "An error has occurred. Please retry.",
        'failed_effect': "Couldn't apply effect.",
        'not_enough_cash': "You don't have enough money! Type /cash to reset it.",
        'you_lost': "You lost...",
        'you_won': "You won {:0.2f}$!",
        'cash_result': " Your money: {:0.2f}$.",
        'reroll': "Reroll (-{:0.2f}$)",
        'summary': "You bet {}$ and won a total of {}$.",
        'current_bet': "{}, your current bet is {:0.2f}$.",
        'current_cash': "{}, you currently have {:0.2f}$ in your account.",
        'cash_reset': "{}, your cash has been reset to {:0.2f}$. You can do this once per day.",
        'cash_reset_fail': "{}, you have {:0.2f}$ in your account and you cannot reset it today. Come back tomorrow.",
        'no_autospin': "Sorry, multiple spins are disabled in group chats.",
        'current_language': "Current language: {}.\nChoices: {}\nTo change it, type \"/lang <code>\" or use one of the buttons below.",
        'invalid_language': "Invalid language.",
        'language_set': "Language set: {}",
        'none_callback': "This button does nothing.",
        'fast_output': "Win: {:0.2f}$",
        'repeat_autospin': "Spin {} times again (-{:0.2f}$)"
    },
    'it': {
        'name': "Italiano",
        'emoji' : "🇮🇹",
        'welcome' : "Benvenuto da PILuAnimeBot!",
        'sauce' : "Salsa 🍝",
        'no_caption' : "Scrivi un testo per favore.",
        'lewd_toggle' : "La roba lewd è stata {} per questa chat.",
        'enabled' : "abilitata",
        'disabled' : "disabilitata",
        'unknown' : "Non ho capito.",
        'error': "Qualcosa è andato storto, riprova.",
        'failed_effect': "Impossibile applicare l'effetto.",
        'not_enough_cash': "Saldo insufficiente! Usa /cash per ripristinarlo.",
        'you_lost': "Hai perso...",
        'you_won': "Hai vinto {:0.2f}€!",
        'cash_result': " Saldo: {:0.2f}€.",
        'reroll': "Riprova (-{:0.2f}€)",
        'summary': "Hai giocato {}€ e vinto un totale di {}€.",
        'current_bet': "{}, il tuo bet attuale è {:0.2f}€.",
        'current_cash': "{}, il tuo saldo attuale è {:0.2f}€.",
        'cash_reset': "{}, il tuo saldo è stato ripristinato a {:0.2f}€. Puoi farlo una volta al giorno.",
        'cash_reset_fail': "{}, il tuo saldo è {:0.2f}€ e non puoi più resettarlo oggi. Riprova domani.",
        'no_autospin': "Gli spin multipli sono disabilitati nelle chat di gruppo.",
        'current_language': "Lingua attuale: {}.\nAltre lingue: {}\nPer cambiarla, scrivi \"/lang <codice>\" o usa uno dei tasti qui sotto.",
        'invalid_language': "Questa lingua non esiste.",
        'language_set': "Lingua impostata: {}",
        'none_callback': "Questo tasto non fa nulla.",
        'fast_output': "Vinto: {:0.2f}€",
        'repeat_autospin': "Altri {} spin (-{:0.2f}€)"
    },
}
langs = localization.keys()
default_lang = "en"

n_entries = len(localization[default_lang].keys())
        
#markup = InlineKeyboardMarkup([[button, button][button, button]])

def format_lang(lang: str):
    try:
        return f"{localization[lang]['name']} {localization[lang]['emoji']}"
    except KeyError:
        return 'Unknown'

buttons = []
for i in langs:
    assert(n_entries == len(localization[i].keys()))
    buttons.append(InlineKeyboardButton(text=format_lang(i), callback_data=f"set_lang_{i}"))

N = 2
lang_markup = InlineKeyboardMarkup([buttons[n:n+N] for n in range(0, len(buttons), N)])

def format_author(user: User):
    if user.username is not None:
        return user.full_name + f" ({user.username})"
    return user.full_name

def format_chat(chat: Chat):
    return chat.title + ("" if chat.username is None else f" ({chat.username})")

def get_lang(context: CallbackContext):
    try:
        return context.chat_data["lang"]
    except KeyError:
        context.chat_data["lang"] = default_lang
        return default_lang

def get_localized_string(text:str, context:CallbackContext):
    lang = get_lang(context)
    
    try:
        return localization[lang][text]
    except KeyError:
        logging.error("No text was found.")
        return "localization error {}{}{}{}{}{}"

slot_machine_value = {
    1: (3, "bar"),
    2: (2, "bar"),
    3: (2, "bar"),
    4: (2, "bar"),
    5: None,
    6: (2, "grape"),
    7: None,
    8: None,
    9: None,
    10: None,
    11: (2, "lemon"),
    12: None,
    13: None,
    14: None,
    15: None,
    16: (2, "seven"),
    17: (2, "bar"),
    18: None,
    19: None,
    20: None,
    21: (2, "grape"),
    22: (3, "grape"),
    23: (2, "grape"),
    24: (2, "grape"),
    25: None,
    26: None,
    27: (2, "lemon"),
    28: None,
    29: None,
    30: None,
    31: None,
    32: (2, "seven"),
    33: (2, "bar"),
    34: None,
    35: None,
    36: None,
    37: None,
    38: (2, "grape"),
    39: None,
    40: None,
    41: (2, "lemon"),
    42: (2, "lemon"),
    43: (3, "lemon"),
    44: (2, "lemon"),
    45: None,
    46: None,
    47: None,
    48: (2, "seven"),
    49: (2, "bar"),
    50: None,
    51: None,
    52: None,
    53: None,
    54: (2, "grape"),
    55: None,
    56: None,
    57: None,
    58: None,
    59: (2, "lemon"),
    60: None,
    61: (2, "seven"),
    62: (2, "seven"),
    63: (2, "seven"),
    64: (3, "seven"),
}

win_table = {
    (3, "seven"): 20,
    (3, "bar"): 5,
    (3, "lemon"): 3,
    (3, "grape"): 2,
    
    (2, "seven"): 2,
    (2, "bar"): 1,
    (2, "lemon"): 0.5,
    (2, "grape"): 0.3
}
