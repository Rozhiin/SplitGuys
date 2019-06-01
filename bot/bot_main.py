from telegram import Update, Bot, Message
from enum import Enum


class CommandType(Enum):
    START = 0,
    ADDCOST = 1,

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
        bot.sendMessage(message.chat.id, "هزینه " + message.text + " برای کاربر با آی‌دی ِ" +
                        message.from_user.username + " ثبت شد.")
        # TODO: states must be saved in cache table


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
