from telegram import Update, Bot, Message, CallbackQuery
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share
from bot.bot_messages import *
from bot.bot_functions import *


def bot_register(bot, message, command):
    delete_states_and_caches(group_id=message.chat.id, user_id=message.from_user.id)
    try:
        member = Member.objects.get(group_id=message.chat.id, user_id=message.from_user.id)
        send_message_already_registered(bot, message.chat.id)
        return
    except Member.DoesNotExist:
        state = State(group_id=message.chat.id, user_id=message.from_user.id,
                      last_command=command.value[0], command_state=0)
        state.save()
        send_message_send_card_number(bot, message.chat.id)


def handle_register_reply(bot: Bot, data, state):
    if not isinstance(data, Message):
        send_message_not_a_message(bot, data.message.chat.id)
    message = data
    if not message.text.isdigit():
        send_message_card_number_not_digit(bot, message.chat.id)
        return
    if len(message.text) < 16:
        send_message_card_number_low(bot, message.chat.id)
        return
    if len(message.text) > 16:
        send_message_card_number_high(bot, message.chat.id)
        return
    member = Member(group_id=message.chat.id, user_id=message.from_user.id, card_number="_")
    member.card_number = message.text
    member.save()
    send_message_user_registered(bot, message.chat.id)
    delete_states_and_caches(message.chat.id, message.from_user.id)
