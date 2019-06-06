from bot.bot_commands.bot_addcost import *
from bot.bot_commands.bot_register import *

class CommandType(Enum):
    REGISTER = 0,
    ADDCOST = 1,  # 0:waiting for value 1:value received waiting for share type

    def get_text(self):
        return '/' + self.name.lower()


def handle_update(bot, update):
    # update = Update()
    # bot = Bot()
    if update.message is None:
        handle_reply(bot, update.callback_query)
    elif update.message.chat.type == 'supergroup':
        handle_group_message(bot, update.message)
    elif update.message.chat.type == 'private':
        handle_private_message(bot, update.message)


def handle_group_message(bot, message):
    # bot = Bot()
    # message = Message()
    if message.text.startswith('/'):
        handle_group_command(bot, message)
    else:
        handle_reply(bot, message)


def handle_private_message(bot, message):
    if message.text.startswith('/getmydebt'):
        result = 0
        costs = Cost.objects.filter(payer_id=message.from_user.id)
        for cost in costs:
            result -= cost.amount

        shares = Share.objects.filter(user_id=message.from_user.id)
        for share in shares:
            result += share.share

        send_message_mydebt(bot, message.chat.id, result)

    else:
        send_message_private_chat(bot, message.chat.id)


def handle_group_command(bot, message):
    command_type = CommandType.REGISTER
    for type in CommandType:
        if message.text.startswith(type.get_text()):
            command_type = type
            break
    if command_type == CommandType.REGISTER:
        bot_register(bot, message)
    elif command_type == CommandType.ADDCOST:
        last_states = State.objects.filter(group_id=message.chat.id, user_id=message.from_user.id)
        for state in last_states:
            state.delete()
        state = State(group_id=message.chat.id, user_id=message.from_user.id,
                      last_command=CommandType.ADDCOST.value[0], command_state=0)
        state.save()
        send_message_send_cost(bot, message.chat.id)


def handle_reply(bot, data):
    chat_id = 0
    user_id = 0
    if isinstance(data, Message):
        chat_id = data.chat.id
        user_id = data.from_user.id
    elif isinstance(data, CallbackQuery):
        chat_id = data.message.chat.id
        user_id = data.from_user.id
    try:
        state = State.objects.get(group_id=chat_id, user_id=user_id)
    except:
        send_message_reply_without_state_error(bot, chat_id)
        return
    if state.last_command == CommandType.ADDCOST.value[0]:
        handle_addcost_reply(bot, data, state)
