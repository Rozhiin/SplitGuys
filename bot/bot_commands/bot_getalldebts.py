from bot.models import Share, Cost, Member
from bot.bot_functions import *
from bot.bot_messages import *


def bot_getalldebts(bot, message):
    owe = {}
    payment = []
    # a=Cost.objects.get(group_id=message.chat.id)
    for cost in Cost.objects.filter(group_id=message.chat.id):
        if cost.payer_id not in owe:
            owe[cost.payer_id] = [0, 0]
        owe[cost.payer_id][0] += cost.amount
        for share in Share.objects.filter(cost=cost):
            if share.user_id not in owe:
                owe[share.user_id] = [0, 0]

            owe[share.user_id][1] += share.share

    for person in owe:
        min_ = min(owe.get(person)[0], owe.get(person)[1])
        owe[person] = [owe.get(person)[0] - min_, owe.get(person)[1] - min_]

    owe_list = list(owe.keys())
    it1, it2 = 0, 0
    while it1 < len(owe_list):
        while owe.get(owe_list[it1])[1] > 0:
            if owe.get(owe_list[it2])[0] == 0:
                it2 += 1
            min_ = min(owe.get(owe_list[it1])[1], owe.get(owe_list[it2])[0])
            if min_ == 0:
                continue
            payment += [[owe_list[it1], owe_list[it2], min_]]
            owe[owe_list[it1]] = [0, owe.get(owe_list[it1])[1] - min_]
            owe[owe_list[it2]] = [owe.get(owe_list[it2])[0] - min_, 0]

        it1 += 1
    # payement_print = ''
    # for pay in payment:
    #     payement_print += '\n' + "\t".join(map(str, pay))

    # bot.sendMessage(message.chat.id, payement_print)
    pay = make_payement_with_username(payment, message, bot)
    send_message_getalldebts(bot, message.chat.id, pay)
    return
    

def make_payement_with_username(payemet, message, bot_):
    res = []
    for pay in payemet:
        member1 = Member.objects.get(group_id=message.chat.id, user_id=pay[0])
        member2 = Member.objects.get(group_id=message.chat.id, user_id=pay[1])
        users = get_users_from_members(bot_, [member1, member2])
        res += [[users[0].username, users[1].username, pay[2], member2.card_number]]

    return res

