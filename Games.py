from telegram import Update, Dice, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from datetime import date
import Constants as c
import time

lastreset_default = date(1970, 1, 1)
saldo_default = 10000
bet_default = 50
slot_emoji = '🎰'

def set_user_value(context: CallbackContext, key:str, amount):
    context.user_data[key] = amount
    return amount

def get_user_value(context: CallbackContext, key:str, default):
    try:
        return context.user_data[key]
    except KeyError:
        print(f"set {key} to {str(default)}")
        return set_user_value(context, key, default)

def get_saldo(context: CallbackContext):
    saldo = get_user_value(context, "saldo", saldo_default)
    
    if saldo == 0:
        lastreset = get_lastreset(context)
        today = date.today()
        
        if lastreset < today:
            set_lastreset(context, today)
            saldo = set_saldo(context, saldo_default)

    return saldo

def set_saldo(context: CallbackContext, amount: int):
    return set_user_value(context, "saldo", amount)

def get_bet(context: CallbackContext):
    return get_user_value(context, "bet", bet_default)

def set_lastreset(context: CallbackContext, amount: int):
    return set_user_value(context, "lastreset", amount)

def get_lastreset(context: CallbackContext):
    return get_user_value(context, "lastreset", lastreset_default)
    
def set_bet(context: CallbackContext, amount: int):
    return set_user_value(context, "bet", amount)

def _spin(context: CallbackContext, id: float, markup: InlineKeyboardMarkup = ""):

    bet = get_bet(context)
    saldo = get_saldo(context)
    
    if saldo < bet:
        context.bot.send_message(chat_id=id, text="Saldo esaurito!")
        return None
    
    saldo = set_saldo(context, saldo - bet)
    
    message = context.bot.send_dice(chat_id=id, emoji=slot_emoji)
    
    values = c.get_symbols(message.dice.value)
    values_count = {i:values.count(i) for i in values}
    
    symbol = max(values_count, key=values_count.get)
    
    win = bet * c.get_multiplier(count=values_count[symbol], symbol=symbol)
    
    saldo = set_saldo(context, saldo + win)
        
    text = "Hai perso..." if win == 0 else "Hai vinto {}€!".format(win / 100)
    
    text += " Saldo: {}€.".format(saldo / 100)
    
    time.sleep(2)
    context.bot.send_message(chat_id=id, text=text, reply_markup=markup)
    return win

def spin(update: Update, context: CallbackContext):
    
    bet = get_bet(context) / 100
    
    try:
        amount = int(context.args[0])
    except (TypeError, IndexError):
        amount = 1
    
    if amount == 1:
        
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Reroll (-{}€)".format(bet), callback_data="callback_1")]])
        _spin(context=context, id=update.effective_chat.id, markup=markup)
    else:
        count = 0
        total_win = 0
        for i in range(amount):
            win = _spin(context=context, id=update.effective_chat.id, markup="")
            
            if win is None:
                break
            
            count += 1
            total_win += win
        
        result = "Hai giocato {}€ e vinto un totale di {}€".format(count * bet, total_win / 100)
        markup = "" #InlineKeyboardMarkup([[InlineKeyboardButton(text="Altri {} spin (-{}€)".format(amount, bet * amount), callback_data="callback_2")]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=markup)
    
    
    
    
def spin_5(update: Update, context: CallbackContext):
    bet = get_bet(context) / 100
    amount = 5
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Altri {} spin (-{}€)".format(amount, bet * amount), callback_data="callback_2")]])
    
    _autospin(context=context, id=update.effective_chat.id, amount=5, markup=markup)
