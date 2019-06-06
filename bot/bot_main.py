from telegram import Update, Bot, Message, CallbackQuery
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share
from bot.bot_messages import *


class CommandType(Enum):
    START = 0,
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


def handle_addcost_reply(bot, data, state):
    if state.command_state == 0:
        if not isinstance(data, Message):
            send_message_not_a_message(bot, data.message.chat.id)
            return
        message = data
        if not message.text.isdigit():
            send_message_not_a_number_error(bot, message.chat.id)
            return
        caches = Cache.objects.filter(group_id=message.chat.id, user_id=message.from_user.id,
                                      var_name="cost_value")
        for cache in caches:
            cache.delete()
        cache = Cache(group_id=message.chat.id, user_id=message.from_user.id,
                      var_name="cost_value", value=float(message.text))
        cache.save()
        state.command_state = 1
        state.save()
        send_message_select_cost_kind(bot, message.chat.id)
    #TODO: send name of cost
    elif state.command_state == 1:
        if not isinstance(data, CallbackQuery):
            send_message_not_a_callback(bot, data.chat.id)
            return
        callback = data
        if callback.data == "0":
            members = Member.objects.filter(group_id=callback.message.chat.id)
            if len(members) == 0:
                send_message_have_not_members(bot, callback.message.chat.id)
                return
            cost_value = 0
            try:
                cost_value = Cache.objects.get(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                      var_name="cost_value")
                cost_value = cost_value.value
            except:
                send_message_cache_not_found(bot, callback.message.chat.id)
                return
            cost_share = cost_value//len(members)
            cost = Cost(name="test", group_id=callback.message.chat.id, payer_id=callback.from_user.id,
                        amount= cost_value, description="test")
            cost.save()
            for member in members:
                share = Share(cost=cost, user_id=callback.from_user.id, share=cost_share)
                share.save()
            caches = Cache.objects.filter(group_id=callback.message.chat.id, user_id=callback.from_user.id)
            for cache in caches:
                cache.delete()
            last_states = State.objects.filter(group_id=callback.message.chat.id, user_id=callback.from_user.id)
            for state in last_states:
                state.delete()
            send_message_added_cost(bot, callback.message.chat.id)
        elif callback.data == "1":
            #TODO
            pass
        else:
            #TODO
            pass
