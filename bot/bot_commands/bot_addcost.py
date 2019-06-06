from telegram import Update, Bot, Message, CallbackQuery
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share
from bot.bot_messages import *


def handle_addcost_reply(bot, data, state):  # data is message or callback_query object
    if state.command_state == 0:
        handle_state_0(bot, data, state)
    elif state.command_state == 1:
        handle_state_1(bot, data, state)
    elif state.command_state == 2:
        handle_state_2(bot, data, state)


def handle_state_0(bot, data, state):
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
    send_message_get_name(bot, message.chat.id)


def handle_state_1(bot, data, state):
    if not isinstance(data, Message):
        send_message_not_a_message(bot, data.message.chat.id)
    message = data
    caches = Cache.objects.filter(group_id=message.chat.id, user_id=message.from_user.id,
                                  var_name="cost_name")
    for cache in caches:
        cache.delete()
    cache = Cache(group_id=message.chat.id, user_id=message.from_user.id,
                  var_name="cost_name", string_value=message.text)
    cache.save()
    state.command_state = 2
    state.save()
    send_message_select_cost_kind(bot, message.chat.id)


def handle_state_2(bot, data, state):
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
        cost_name = "empty"
        try:
            cost_value = Cache.objects.get(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                                           var_name="cost_value")
            cost_value = cost_value.value
            cost_name = Cache.objects.get(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                                           var_name="cost_name").string_value
        except:
            send_message_cache_not_found(bot, callback.message.chat.id)
            return
        cost_share = cost_value // len(members)
        cost = Cost(name=cost_name, group_id=callback.message.chat.id, payer_id=callback.from_user.id,
                    amount=cost_value, description="test")
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
        # TODO
        pass
    else:
        # TODO
        pass
