import logging

localization = {
    'us': {
        'welcome' : "Welcome to PILuAnimeBot!",
        'sauce' : "Sauce 🍝",
        'no_caption' : "No caption detected.",
        'lewd_toggle' : "Lewd content was {} for this chat.",
        'enabled' : "enabled",
        'disabled' : "disabled",
        'unknown' : "Sorry, I didn't understand that command.",
        'error': "An error has occurred. Please retry.",
        'failed_effect': "Couldn't apply effect."
    },
    'it': {
        'welcome' : "Benvenuto da PILuAnimeBot!",
        'sauce' : "Salsa 🍝",
        'no_caption' : "Scrivi un testo per favore.",
        'lewd_toggle' : "La roba lewd è stata {} per questa chat.",
        'enabled' : "abilitata",
        'disabled' : "disabilitata",
        'unknown' : "Non ho capito.",
        'error': "Qualcosa è andato storto, riprova.",
        'failed_effect': "Impossibile applicare l'effetto."
    },
}


def get_localized_string(text, lang='us'):
    try:
        return localization[lang][text]
    except KeyError:
        logging.error("No text was found.")
        return "localization error {}{}{}{}{}{}"