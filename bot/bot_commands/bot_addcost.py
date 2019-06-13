from telegram import Update, Bot, Message, CallbackQuery, User
from enum import Enum
from bot.models import State, Cache, Member, Cost, Share
from bot.bot_messages import *
from bot.bot_functions import *


# states:
# 0: waiting for cost value
# 1: waiting for cost name
# 2: waiting for cost division type
# 3: division type 1 - waiting for users list
# 4: division type 2 - watiing for user share


def handle_addcost_reply(bot, data, state):  # data is message or callback_query object
    if state.command_state == 0:
        handle_state_0(bot, data, state)
    elif state.command_state == 1:
        handle_state_1(bot, data, state)
    elif state.command_state == 2:
        handle_state_2(bot, data, state)
    elif state.command_state == 3:
        handle_state_3(bot, data, state)
    elif state.command_state == 4:
        handle_state_4(bot, data, state)


def handle_state_0(bot, data, state):
    if not isinstance(data, Message):
        send_message_not_a_message(bot, data.message.chat.id)
        return
    message = data
    try:
        float(message.text)
    except ValueError:
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
        handle_state_2_callback_0(bot, callback, state)
    elif callback.data == "1":
        handle_state_2_callback_1(bot, callback, state)
    else:
        handle_state_2_callback_2(bot, callback, state)
        pass


def handle_state_2_callback_0(bot, callback, state):
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
    except Cache.DoesNotExist:
        send_message_cache_not_found(bot, callback.message.chat.id)
        return
    cost_share = cost_value / len(members)
    cost = Cost(name=cost_name, group_id=callback.message.chat.id, payer_id=callback.from_user.id,
                amount=cost_value, description="test")
    cost.save()
    for member in members:
        share = Share(cost=cost, user_id=member.user_id, share=cost_share)
        share.save()
    delete_states_and_caches(group_id=callback.message.chat.id, user_id=callback.from_user.id)
    send_message_added_cost(bot, callback.message.chat.id)


def handle_state_2_callback_1(bot, callback, state):
    state.command_state = 3
    state.save()
    members = Member.objects.filter(group_id=callback.message.chat.id)
    if len(members) == 0:
        delete_states_and_caches(group_id=callback.message.chat.id, user_id=callback.from_user.id)
        send_message_have_not_members(bot, callback.message.chat.id)
        return
    users = get_users_from_members(bot, members)
    message_id = send_message_select_users(bot, callback.message.chat.id, users, [])
    cache = Cache(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                  var_name="message_users_id", string_value=message_id)
    # TODO: make var names in a list
    cache.save()


def handle_state_3(bot, data, state):
    if not isinstance(data, CallbackQuery):
        send_message_not_a_callback(bot, data.chat.id)
        return
    callback = data
    if callback.data == "ended":
        handle_state_3_ended(bot, callback, state)
    else:
        message_id = ""
        try:
            cache_message_id = Cache.objects.get(group_id=callback.message.chat.id,
                                                 user_id=callback.from_user.id,
                                                 var_name="message_users_id")
            message_id = cache_message_id.string_value
        except Cache.DoesNotExist:
            send_message_cache_not_found(bot, callback.message.chat.id)
            return
        try:
            cache_user = Cache.objects.get(group_id=callback.message.chat.id,
                                           user_id=callback.from_user.id,
                                           var_name="cost_user", string_value=callback.data)
            cache_user.delete()
        except Cache.DoesNotExist:
            cache_user = Cache(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                               var_name="cost_user", string_value=callback.data)
            cache_user.save()
        members = Member.objects.filter(group_id=callback.message.chat.id)
        if len(members) == 0:
            delete_states_and_caches(group_id=callback.message.chat.id, user_id=callback.from_user.id)
            send_message_have_not_members(bot, callback.message.chat.id)
            return
        users = get_users_from_members(bot, members)
        selecteds = []
        user_caches = Cache.objects.filter(group_id=callback.message.chat.id,
                                           user_id=callback.from_user.id,
                                           var_name="cost_user")
        for user_cache in user_caches:
            selecteds.append(user_cache.string_value)
        send_message_select_users(bot, callback.message.chat.id, users, selecteds, message_id=message_id)


def handle_state_3_ended(bot, callback, state):
    members = []
    cost_users = Cache.objects.filter(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                                      var_name="cost_user")
    for cost_user in cost_users:
        members.append(Member(group_id=callback.message.chat.id, user_id=cost_user.string_value))
    if len(members) == 0:
        send_message_have_not_selected_users(bot, callback.message.chat.id)
        return
    cost_value = 0
    cost_name = "empty"
    try:
        cost_value = Cache.objects.get(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                                       var_name="cost_value")
        cost_value = cost_value.value
        cost_name = Cache.objects.get(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                                      var_name="cost_name").string_value
    except Cache.DoesNotExist:
        send_message_cache_not_found(bot, callback.message.chat.id)
        return
    cost_share = cost_value / len(members)
    cost = Cost(name=cost_name, group_id=callback.message.chat.id, payer_id=callback.from_user.id,
                amount=cost_value, description="test")
    cost.save()
    for member in members:
        share = Share(cost=cost, user_id=member.user_id, share=cost_share)
        share.save()
    delete_states_and_caches(group_id=callback.message.chat.id, user_id=callback.from_user.id)
    send_message_added_cost(bot, callback.message.chat.id)


def handle_state_2_callback_2(bot, callback, state):
    state.command_state = 4
    state.save()
    cache = Cache(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                  var_name="custom_index", value=0)
    # TODO: make var names in a list
    cache.save()
    cache = Cache(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                  var_name="custom_sum", value=0)
    cache.save()
    members = Member.objects.filter(group_id=callback.message.chat.id).exclude(user_id=callback.from_user.id).order_by(
        'user_id')
    users = get_users_from_members(bot, members)
    if len(users) != 0:
        send_message_send_every_user_share(bot, callback.message.chat.id)
        send_message_username(bot, callback.message.chat.id, users[0].username)
    else:
        try:
            cost_value = Cache.objects.get(group_id=callback.message.chat.id, user_id=callback.from_user.id,
                                           var_name="cost_value")
            cost_value = cost_value.value
        except Cache.DoesNotExist:
            send_message_cache_not_found(bot, callback.message.chat.id)
            return
        user_cache = Cache(group_id=callback.message.chat.id,
                           user_id=callback.from_user.id,
                           var_name="custom_" + str(callback.from_user.id), value=cost_value)
        user_cache.save()
        send_message_remaining(bot, callback.message.chat.id, cost_value)
        handle_state_4_ended(bot, callback, state)


def handle_state_4(bot, data, state):
    if not isinstance(data, Message):
        send_message_not_a_message(bot, data.message.chat.id)
        return
    message = data
    # TODO: this part is repeated and can be in a function
    members = Member.objects.filter(group_id=message.chat.id).exclude(user_id=message.from_user.id).order_by('user_id')
    users = get_users_from_members(bot, members)
    # end of part
    try:
        custom_index_cache = Cache.objects.get(group_id=message.chat.id,
                                               user_id=message.from_user.id,
                                               var_name="custom_index")
        custom_index = int(custom_index_cache.value)
        cost_value = Cache.objects.get(group_id=message.chat.id,
                                       user_id=message.from_user.id,
                                       var_name="cost_value")
        cost_value = cost_value.value
        custom_sum_cache = Cache.objects.get(group_id=message.chat.id,
                                             user_id=message.from_user.id,
                                             var_name="custom_sum")
    except Cache.DoesNotExist:
        send_message_cache_not_found(bot, message.chat.id)
        return
    try:
        float(message.text)
    except ValueError:
        send_message_not_a_number_error(bot, message.chat.id)
        return
    try:
        user_share = float(message.text)
        if custom_sum_cache.value + user_share > cost_value:
            send_message_share_exceeded(bot, message.chat.id)
            return
        user_id = str(users[custom_index].id)
        user_cache = Cache(group_id=message.chat.id,
                           user_id=message.from_user.id,
                           var_name="custom_" + user_id, value=user_share)
        user_cache.save()
        custom_sum_cache.value = custom_sum_cache.value + user_share
        custom_sum_cache.save()
        custom_index_cache.value = custom_index + 1
        custom_index_cache.save()
        next_user_name = users[custom_index + 1].username
        send_message_username(bot, message.chat.id, next_user_name)
    except IndexError:
        user_cache = Cache(group_id=message.chat.id,
                           user_id=message.from_user.id,
                           var_name="custom_" + str(message.from_user.id), value=cost_value - custom_sum_cache.value)
        user_cache.save()
        send_message_remaining(bot, message.chat.id, cost_value - custom_sum_cache.value)
        handle_state_4_ended(bot, message, state)


# TODO: ends have been repeated. can be a function
def handle_state_4_ended(bot, data, state):
    if isinstance(data, Message):
        group_id = data.chat.id
    else:
        group_id = data.message.chat.id
    user_id = data.from_user.id
    members = Member.objects.filter(group_id=group_id).order_by('user_id')
    if len(members) == 0:
        delete_states_and_caches(group_id=group_id, user_id=user_id)
        send_message_have_not_members(bot, group_id)
        return
    users = get_users_from_members(bot, members)
    cost_value = 0
    cost_name = "empty"
    try:
        cost_value = Cache.objects.get(group_id=group_id, user_id=user_id,
                                       var_name="cost_value")
        cost_value = cost_value.value
        cost_name = Cache.objects.get(group_id=group_id, user_id=user_id,
                                      var_name="cost_name").string_value
    except Cache.DoesNotExist:
        send_message_cache_not_found(bot, group_id)
        return
    cost = Cost(name=cost_name, group_id=group_id, payer_id=user_id,
                amount=cost_value, description="test")
    cost.save()
    for user in users:
        try:
            custom_cache = Cache.objects.get(group_id=group_id,
                                             user_id=user_id,
                                             var_name="custom_" + str(user.id))
        except Cache.DoesNotExist:
            send_message_cache_not_found(bot, group_id)
            return
        user_share = custom_cache.value
        share = Share(cost=cost, user_id=user.id, share=user_share)
        share.save()
    delete_states_and_caches(group_id=group_id, user_id=user_id)
    send_message_added_cost(bot, group_id)


