import telegram

from bot.models import Cache, State

from enum import Enum


class MarketType(Enum):
    RESTAURANT = 0,
    CAFE = 1,
    CINEMA = 2,


market_type_names = ["رستوران", "کافه", "سینما"]


def delete_states_and_caches(group_id, user_id):
    caches = Cache.objects.filter(group_id=group_id, user_id=user_id)
    for cache in caches:
        cache.delete()
    last_states = State.objects.filter(group_id=group_id, user_id=user_id)
    for state in last_states:
        state.delete()


def get_users_from_members(bot, members):
    try:
        users = []
        for member in members:
            cm = bot.get_chat_member(chat_id=member.group_id, user_id=member.user_id)
            users.append(cm.user)
        return users
    except telegram.error.BadRequest:
        print("error: telegram bad request")
        return []
