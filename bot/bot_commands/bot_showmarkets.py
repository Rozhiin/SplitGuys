from telegram import Update, Bot, Message, CallbackQuery, User
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share, Market
from bot.bot_messages import *
from bot.bot_functions import *


def showmarkets_handle_command(bot: Bot, message, command):
    state = State(group_id=message.chat.id, user_id=message.from_user.id,
                  last_command=command.value[0], command_state=0)
    state.save()
    send_message_select_type(bot, message.chat.id, is_for_customers=True)


def handle_showmarket_reply(bot: Bot, data, state):
    if not isinstance(data, CallbackQuery):
        send_message_not_a_callback(bot, data.chat.id)
    callback = data
    type = callback.data
    markets = Market.objects.filter(type=type)
    send_message_markets(bot, data.message.chat.id, markets)
    delete_states_and_caches(callback.message.chat.id, callback.from_user.id)
