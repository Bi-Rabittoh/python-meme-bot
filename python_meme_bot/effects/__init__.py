
from typing import Callable, Dict, Tuple
from .functions import ttbt_effect, bt_effect, splash_effect, wot_effect, text_effect
from .checks import ttbt_check, tt_check, splash_check, wot_check

HandlerTuple = Tuple[Callable, Callable]

effectsDict: Dict[str, HandlerTuple] = {
    # "effect_name": (effect_check, effect_fn)
    "ttbt": (ttbt_check, ttbt_effect),
    "tt": (tt_check, ttbt_effect),
    "bt": (tt_check, bt_effect),
    "splash": (splash_check, splash_effect),
    "wot": (wot_check, wot_effect),
    "text": (wot_check, text_effect),
}
