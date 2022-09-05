localization = {
    'us': {
        'welcome' : "Welcome to PILuAnimeBot!",
        'sauce' : "[Sauce 🍝]({})",
        'no_caption' : "No caption detected.",
        'lewd_toggle' : "Lewd content was {} for this chat.",
        'enabled' : "enabled",
        'disabled' : "disabled",
        'unknown' : "Sorry, I didn't understand that command.",
        'error': "Something bad happened. Please retry.",
    }
}


def get_localized_string(text, lang='us'):
    try:
        return localization[lang][text]
    except KeyError:
        logging.error("No text was found.")
        return "localization error {}{}{}{}{}{}"