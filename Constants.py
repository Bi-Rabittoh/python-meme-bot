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

symbols = {
    "grape",
    "lemon",
    "bar",
    "seven"
}

slot_machine_value = {
    1: ("bar", "bar", "bar"),
    2: ("grape", "bar", "bar"),
    3: ("lemon", "bar", "bar"),
    4: ("seven", "bar", "bar"),
    5: ("bar", "grape", "bar"),
    6: ("grape", "grape", "bar"),
    7: ("lemon", "grape", "bar"),
    8: ("seven", "grape", "bar"),
    9: ("bar", "lemon", "bar"),
    10: ("grape", "lemon", "bar"),
    11: ("lemon", "lemon", "bar"),
    12: ("seven", "lemon", "bar"),
    13: ("bar", "seven", "bar"),
    14: ("grape", "seven", "bar"),
    15: ("lemon", "seven", "bar"),
    16: ("seven", "seven", "bar"),
    17: ("bar", "bar", "grape"),
    18: ("grape", "bar", "grape"),
    19: ("lemon", "bar", "grape"),
    20: ("seven", "bar", "grape"),
    21: ("bar", "grape", "grape"),
    22: ("grape", "grape", "grape"),
    23: ("lemon", "grape", "grape"),
    24: ("seven", "grape", "grape"),
    25: ("bar", "lemon", "grape"),
    26: ("grape", "lemon", "grape"),
    27: ("lemon", "lemon", "grape"),
    28: ("seven", "lemon", "grape"),
    29: ("bar", "seven", "grape"),
    30: ("grape", "seven", "grape"),
    31: ("lemon", "seven", "grape"),
    32: ("seven", "seven", "grape"),
    33: ("bar", "bar", "lemon"),
    34: ("grape", "bar", "lemon"),
    35: ("lemon", "bar", "lemon"),
    36: ("seven", "bar", "lemon"),
    37: ("bar", "grape", "lemon"),
    38: ("grape", "grape", "lemon"),
    39: ("lemon", "grape", "lemon"),
    40: ("seven", "grape", "lemon"),
    41: ("bar", "lemon", "lemon"),
    42: ("grape", "lemon", "lemon"),
    43: ("lemon", "lemon", "lemon"),
    44: ("seven", "lemon", "lemon"),
    45: ("bar", "seven", "lemon"),
    46: ("grape", "seven", "lemon"),
    47: ("lemon", "seven", "lemon"),
    48: ("seven", "seven", "lemon"),
    49: ("bar", "bar", "seven"),
    50: ("grape", "bar", "seven"),
    51: ("lemon", "bar", "seven"),
    52: ("seven", "bar", "seven"),
    53: ("bar", "grape", "seven"),
    54: ("grape", "grape", "seven"),
    55: ("lemon", "grape", "seven"),
    56: ("seven", "grape", "seven"),
    57: ("bar", "lemon", "seven"),
    58: ("grape", "lemon", "seven"),
    59: ("lemon", "lemon", "seven"),
    60: ("seven", "lemon", "seven"),
    61: ("bar", "seven", "seven"),
    62: ("grape", "seven", "seven"),
    63: ("lemon", "seven", "seven"),
    64: ("seven", "seven", "seven"),
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

def get_symbols(value: int):
    try:
        return slot_machine_value[value]
    except IndexError:
        return slot_machine_value[50]

def get_multiplier(count: int, symbol: str):
    try:
        return win_table[(count, symbol)]
    except KeyError as e:
        return 0

def get_localized_string(text, lang='us'):
    try:
        return localization[lang][text]
    except KeyError:
        logging.error("No text was found.")
        return "localization error {}{}{}{}{}{}"
    