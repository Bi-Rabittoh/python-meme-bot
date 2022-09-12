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
        'failed_effect': "Couldn't apply effect.",
        'not_enough_cash': "You don't have enough money!",
        'you_lost': "You lost...",
        'you_won': "You won {:0.2f}$!",
        'cash_result': " Your money: {:0.2f}$.",
        'reroll': "Reroll (-{:0.2f}$)",
        'summary': "You bet {}$ and won a total of {}$.",
        'current_bet': "{}, your current bet is {:0.2f}$.",
        'current_cash': "{}, you currently have {:0.2f}$ in your account.",
        'no_autospin': "Sorry, multiple spins are disabled in group chats."
        
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
        'failed_effect': "Impossibile applicare l'effetto.",
        'not_enough_cash': "Saldo insufficiente!",
        'you_lost': "Hai perso...",
        'you_won': "Hai vinto {:0.2f}€!",
        'cash_result': " Saldo: {:0.2f}€.",
        'reroll': "Riprova (-{:0.2f}€)",
        'summary': "Hai giocato {}€ e vinto un totale di {}€.",
        'current_bet': "{}, il tuo bet attuale è {:0.2f}€.",
        'current_cash': "{}, il tuo saldo attuale è {:0.2f}€.",
        'no_autospin': "Gli spin multipli sono disabilitati nelle chat di gruppo."
    },
}

def format_author(user):
    
    if user.username is not None:
        return user.full_name + f" ({user.username})"
    return user.full_name

def get_localized_string(text, lang='us'):
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
    (3, "seven"): 50,
    (3, "bar"): 20,
    (3, "lemon"): 10,
    (3, "grape"): 5,
    
    (2, "seven"): 10,
    (2, "bar"): 5,
    (2, "lemon"): 2,
    (2, "grape"): 1
}
