from bot.bot_commands.bot_addcost import *
from bot.bot_commands.bot_register import *
from bot.bot_commands.bot_getalldebts import *
from bot.bot_functions import *
from bot.bot_commands.bot_addmarket import *
from bot.bot_commands.bot_showmarkets import *


class CommandType(Enum):
    REGISTER = 0,
    ADDCOST = 1,
    CANCEL = 2,
    GETALLDEBTS = 3,
    SHOWMARKETS = 6,

    def get_text(self):
        return '/' + self.name.lower()


class PvCommand(Enum):
    GETMYDEBT = 4,
    ADDMARKET = 5

    def get_text(self):
        return '/' + self.name.lower()


def handle_update(bot, update):
    # update = Update()
    # bot = Bot()
    if update.message is None:
        if update.callback_query.message.chat.type == 'supergroup':
            handle_reply(bot, update.callback_query)
        if update.callback_query.message.chat.type == 'private':
            handle_private_not_command(bot, update.callback_query)
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
    if message.text.startswith('/'):
        handle_private_command(bot, message)
    else:
        handle_private_not_command(bot, message)


def handle_group_command(bot, message):
    command_type = CommandType.REGISTER

    for type in CommandType:
        if message.text.startswith(type.get_text()):
            command_type = type
            break
    delete_states_and_caches(group_id=message.chat.id, user_id=message.from_user.id)
    if command_type == CommandType.REGISTER:
        bot_register(bot, message, command_type)
    elif command_type == CommandType.ADDCOST:
        state = State(group_id=message.chat.id, user_id=message.from_user.id,
                      last_command=CommandType.ADDCOST.value[0], command_state=0)
        state.save()
        send_message_send_cost(bot, message.chat.id)
    elif command_type == CommandType.CANCEL:
        send_message_canceled(bot, message.chat.id)

    elif command_type == CommandType.GETALLDEBTS:
        bot_getalldebts(bot, message)

    elif command_type == CommandType.SHOWMARKETS:
        showmarkets_handle_command(bot, message, command_type)


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
    except State.DoesNotExist:
        send_message_reply_without_state_error(bot, chat_id)
        return
    if state.last_command == CommandType.ADDCOST.value[0]:
        handle_addcost_reply(bot, data, state)
    elif state.last_command == CommandType.SHOWMARKETS.value[0]:
        handle_showmarket_reply(bot, data, state)
    elif state.last_command == CommandType.REGISTER.value[0]:
        handle_register_reply(bot, data, state)


def handle_private_command(bot, message):
    command_type = None

    for type in PvCommand:
        if message.text.startswith(type.get_text()):
            command_type = type
            break
    delete_states_and_caches(group_id=message.chat.id, user_id=message.from_user.id)
    if command_type == PvCommand.GETMYDEBT:
        result = 0
        costs = Cost.objects.filter(payer_id=message.from_user.id)
        for cost in costs:
            result -= cost.amount

        shares = Share.objects.filter(user_id=message.from_user.id)
        for share in shares:
            result += share.share

        send_message_mydebt(bot, message.chat.id, result)
    elif command_type == PvCommand.ADDMARKET:
        addmarket_handle_command(bot, message, PvCommand.ADDMARKET)
    else:
        send_message_command_not_found(bot, message.chat.id)


def handle_private_not_command(bot, data):
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
    except State.DoesNotExist:
        send_message_private_chat(bot, chat_id)
        return
    if state.last_command == PvCommand.ADDMARKET.value:
        addmarket_handle_message(bot, data, state)
