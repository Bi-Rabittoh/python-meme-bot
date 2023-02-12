from telegram import Update, Dice, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from datetime import date
from Constants import get_localized_string as l
import Constants as c
import time

autospin_cap = 20
lastreset_default = date(1970, 1, 1)
cash_default = 5000
bet_default = 50
slot_emoji = '🎰'

def read_arg(context: CallbackContext, default=None, cast=int):
    try:
        return cast(context.args[0].replace(",", ".").replace("€", ""))
    except (TypeError, IndexError, ValueError):
        return default

def set_user_value(context: CallbackContext, key:str, amount):
    context.user_data[key] = amount
    return amount

def get_user_value(context: CallbackContext, key:str, default):
    try:
        return context.user_data[key]
    except KeyError:
        #print(f"set {key} to {str(default)}")
        return set_user_value(context, key, default)

def get_cash(context: CallbackContext):
    return get_user_value(context, "cash", cash_default)

def set_cash(context: CallbackContext, amount: int):
    return set_user_value(context, "cash", amount)

def get_bet(context: CallbackContext):
    return get_user_value(context, "bet", bet_default)

def set_lastreset(context: CallbackContext, amount: int):
    return set_user_value(context, "lastreset", amount)

def get_lastreset(context: CallbackContext):
    return get_user_value(context, "lastreset", lastreset_default)
    
def set_bet(context: CallbackContext, amount: int):
    return set_user_value(context, "bet", max(0, amount))

async def _spin(context: CallbackContext, id: float, delay=True):

    bet = get_bet(context)
    cash = get_cash(context)
    
    if cash < bet:
        await context.bot.send_message(chat_id=id, text=l("not_enough_cash", context))
        return None
    
    cash = set_cash(context, cash - bet)
    
    message = await context.bot.send_dice(chat_id=id, emoji=slot_emoji, disable_notification=True)
    
    multiplier = get_multiplier(message.dice.value)
    
    win = bet * multiplier
    
    cash = set_cash(context, cash + win)
    
    if delay:
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=l("reroll", context).format(bet / 100), callback_data="reroll 1")]])
        
        text = l("you_lost", context) if multiplier == 0 else l("you_won", context).format(win / 100)
        if bet != 0:
            text += l("cash_result", context).format(cash / 100)

        args = {
            "chat_id": id,
            "text": text,
            "reply_markup": markup
        }
        context.job_queue.run_once(show_result, 2, data=args, name=str(id))
    else:
        message.edit_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton(text=l("fast_output", context).format(win / 100), callback_data="none")]]))
    return win

async def show_result(context: CallbackContext):
    con = context.job.data
    return await context.bot.send_message(chat_id=con["chat_id"], text=con["text"], reply_markup=con["reply_markup"], disable_notification=True)
    
async def spin(update: Update, context: CallbackContext):
    
    bet = get_bet(context) / 100
    
    amount = read_arg(context, 1)
    
    if amount > 1 and update.effective_chat.type != 'private':
        amount = 1
        await context.bot.send_message(chat_id=update.effective_chat.id, text=l("no_autospin", context))
    
    if amount == 1:
        return await _spin(context=context, id=update.effective_chat.id)
    else:
        return await autospin(context=context, id=update.effective_chat.id, amount=amount)
    
async def autospin(context: CallbackContext, id: int, amount: int):
    
    bet = get_bet(context) / 100
    count = 0
    total_win = 0
    amount = max(2, min(autospin_cap, amount))
    
    for i in range(amount):
        
        win = await _spin(context=context, id=id, delay=False)
        
        if win is None:
            break
        
        count += 1
        total_win += win
    
    result = l("summary", context).format(count * bet, total_win / 100)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Altri {} spin (-{}€)".format(amount, bet * amount), callback_data=f"reroll {amount}")]])
    return await context.bot.send_message(chat_id=id, text=result, reply_markup=markup, disable_notification=False)

async def bet(update: Update, context: CallbackContext):
    
    amount = read_arg(context=context, cast=float)
    
    if amount is not None:
        bet = set_bet(context, int(amount * 100))
    else:
        bet = get_bet(context)
    
    result = l("current_bet", context).format(c.format_author(update.effective_user), bet / 100)
    return await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    
def cash(update: Update, context: CallbackContext):
    
    cash = get_cash(context) / 100
    
    if cash < cash_default / 200:
        lastreset = get_lastreset(context)
        today = date.today()
        
        if lastreset < today:
            set_lastreset(context, today)
            cash = set_cash(context, cash_default)
            
            result = l("cash_reset", context).format(c.format_author(update.effective_user), cash / 100)
            return update.message.reply_text(text=result)
        else:
            return update.message.reply_text(text=l("cash_reset_fail", context).format(c.format_author(update.effective_user), cash))
    
    
    result = l("current_cash", context).format(c.format_author(update.effective_user), cash)
    return update.message.reply_text(text=result)
    
def get_multiplier(value: int):
    
    try:
        values = c.slot_machine_value[value]
    except IndexError:
        values = c.slot_machine_value[5]
    
    try:
        return c.win_table[values]
    except KeyError:
        return 0
