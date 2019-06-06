from telegram import Update, Bot, Message, CallbackQuery
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share
from bot.bot_messages import *

def bot_register(bot, message):
    member = Member(group_id=message.chat.id, user_id=message.from_user.id)
    try:
        member.save()
        send_message_user_registered(bot, message.chat.id)
    except:
        send_message_already_registered(bot, message.chat.id)
        return