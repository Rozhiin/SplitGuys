from telegram import Update, Bot, Message
from enum import Enum
from bot.models import States


class CommandType(Enum):
    START = 0,
    ADDCOST = 1, # 0:waiting for value 1:value received waiting for share type

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
        state = States.objects.get(group_id=message.chat.id)
        bot.sendMessage(message.chat.id, state.command_state)


def handle_group_command(bot, message):
    command_type = CommandType.START
    for type in CommandType:
        if message.text.startswith(type.get_text()):
            command_type = type
            break
    if command_type == CommandType.START:
        bot.sendMessage(message.chat.id, "you entered start command")
    elif command_type == CommandType.ADDCOST:
        bot.sendMessage(message.chat.id, "لطفا مقدار هزینه را وارد کنید")
        state = States.objects.get(group_id=message.chat.id)
        state.delete()
        state = States(group_id=message.chat.id, last_command=command_type.value,
                       command_state=0)
        state.save()
