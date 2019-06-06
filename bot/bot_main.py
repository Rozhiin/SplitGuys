from telegram import Update, Bot, Message
from enum import Enum
from bot.models import State, Cache
from bot.bot_messages import *


class CommandType(Enum):
    START = 0,
    ADDCOST = 1,  # 0:waiting for value 1:value received waiting for share type

    def get_text(self):
        return '/' + self.name.lower()


def handle_update(bot, update):
    # update = Update()
    # bot = Bot()
    if update.message.chat.type == 'supergroup':
        handle_group_message(bot, update.message)


def handle_group_message(bot, message):
    # bot = Bot()
    # message = Message()
    if message.text.startswith('/'):
        handle_group_command(bot, message)
    else:
        handle_reply(bot, message)


def handle_group_command(bot, message):
    command_type = CommandType.START
    for type in CommandType:
        if message.text.startswith(type.get_text()):
            command_type = type
            break
    if command_type == CommandType.START:
        bot.sendMessage(message.chat.id, "you entered start command")
    elif command_type == CommandType.ADDCOST:
        last_states = State.objects.filter(group_id=message.chat.id, user_id=message.from_user.id)
        for state in last_states:
            state.delete()
        state = State(group_id=message.chat.id, user_id=message.from_user.id,
                      last_command=CommandType.ADDCOST.value[0], command_state=0)
        state.save()
        send_message_send_cost(bot, message.chat.id)

def handle_reply(bot, message):
    state = State.objects.get(group_id=message.chat.id, user_id=message.from_user.id)
    if state is None:
        send_message_reply_without_state_error(bot, message.chat.id)
        return
    if state.last_command == CommandType.ADDCOST.value[0]:
        handle_addcost_reply(bot, message, state)


def handle_addcost_reply(bot, message, state):
    if state.command_state == 0:
        if not message.text.isdigit():
            send_message_not_a_number_error(bot, message.chat.id)
            return
        cache = Cache(group_id=message.chat.id, user_id=message.from_user.id,
                      var_name="cost_value", value=float(message.text))
        cache.save()
        state.command_state = 1
        state.save()
        

