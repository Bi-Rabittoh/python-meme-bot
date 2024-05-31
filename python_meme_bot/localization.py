import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

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

def get_lang(context: ContextTypes.DEFAULT_TYPE):
    try:
        return context.chat_data["lang"]
    except KeyError:
        context.chat_data["lang"] = default_lang
        return default_lang

def get_localized_string(text:str, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    
    try:
        return localization[lang][text]
    except KeyError:
        logging.error("No text was found.")
        return "localization error {}{}{}{}{}{}"
    
def format_lang(lang: str):
    try:
        return f"{localization[lang]['name']} {localization[lang]['emoji']}"
    except KeyError:
        return 'Unknown'
    
_n_entries = len(localization[default_lang].keys())
_buttons = []
for i in langs:
    assert(_n_entries == len(localization[i].keys()))
    _buttons.append(InlineKeyboardButton(text=format_lang(i), callback_data=f"set_lang_{i}"))

N = 2
lang_markup = InlineKeyboardMarkup([_buttons[n:n+N] for n in range(0, len(_buttons), N)])
