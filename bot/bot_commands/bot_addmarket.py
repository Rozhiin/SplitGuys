from telegram import Update, Bot, Message, CallbackQuery, User
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share, Market
from bot.bot_messages import *
from bot.bot_functions import *


def addmarket_handle_command(bot: Bot, message, pvcommand):
    state = State(group_id=message.chat.id, user_id=message.from_user.id,
                  last_command=pvcommand.value, command_state=0)
    state.save()
    send_message_select_type(bot, message.chat.id)


def addmarket_handle_message(bot: Bot, data, state):
    if state.command_state == 0:
        addmarket_state_0(bot, data, state)
    elif state.command_state == 1:
        addmarket_state_1(bot, data, state)
    elif state.command_state == 2:
        addmarket_state_2(bot, data, state)


def addmarket_state_0(bot: Bot, data, state):
    if not isinstance(data, CallbackQuery):
        send_message_not_a_callback(bot, data.chat.id)
    chat_id = data.message.chat.id
    cache = Cache(group_id=chat_id, user_id=data.from_user.id,
                  var_name="market_type", string_value=data.data)
    cache.save()
    state.command_state = 1
    state.save()
    send_message_send_name(bot, chat_id)


def addmarket_state_1(bot: Bot, data, state):
    if not isinstance(data, Message):
        send_message_not_a_message(bot, data.message.chat.id)
    message = data
    cache = Cache(group_id=message.chat.id, user_id=message.from_user.id,
                  var_name="market_name", string_value=message.text)
    cache.save()
    state.command_state = 2
    state.save()
    send_message_send_desc(bot, message.chat.id)


def addmarket_state_2(bot: Bot, data, state):
    if not isinstance(data, Message):
        send_message_not_a_message(bot, data.message.chat.id)
    message = data
    name_cache = None
    type_cache = None
    try:
        name_cache = Cache.objects.get(group_id=message.chat.id, user_id=message.from_user.id,
                                       var_name="market_name")
        type_cache = Cache.objects.get(group_id=message.chat.id, user_id=message.from_user.id,
                                       var_name="market_type")
    except Cache.DoesNotExist:
        send_message_cache_not_found(bot, message)
    if name_cache is None or type_cache is None:
        send_message_cache_not_found(bot, message)
    market = Market(type=type_cache.string_value, name=name_cache.string_value,
                    desc=message.text)
    market.save()
    send_message_market_saved(bot, message.chat.id)
    delete_states_and_caches(message.chat.id, message.from_user.id)

