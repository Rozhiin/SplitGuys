from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize

def send_message_send_cost(bot, id):
    bot.sendMessage(id, "لطفا مقدار هزینه را وارد کنید")


def send_message_private_chat(bot, id):
    bot.sendMessage(id, "من با تو صحبتی ندارم.")

def send_message_mydebt(bot, id, result):
    if result>0:
        bot.sendMessage(id, emojize("شما %d دلار بدهکار هستید :sunglasses:"%result, use_aliases=True))
    else:
        bot.sendMessage(id, emojize(" شما %d دلار طلبکار هستید :sunglasses: "%(-1 * result), use_aliases=True))

def send_message_reply_without_state_error(bot, id):
    bot.sendMessage(id, "مگه من مسخره توام!")


def send_message_not_a_number_error(bot, id):
    bot.sendMessage(id, "ببین چگونه جان مشوش است عدد بده!")


def send_message_not_a_message(bot, id):
    bot.sendMessage(id, "دکمه نزن بچه!")


def send_message_not_a_callback(bot, id):
    bot.sendMessage(id, "دکمه بزن!")


def send_message_cache_not_found(bot, id):
    bot.sendMessage(id, "برو بگو خودش بیاد!")


def send_message_have_not_members(bot, id):
    bot.sendMessage(id, "هیچ کدام از شما لاشیا ثبت نام نکردید!")


def send_message_added_cost(bot, id):
    bot.sendMessage(id, emojize("باتشکر :rose: :rose:", use_aliases=True))


def send_message_select_cost_kind(bot, id):
    button_list = [
        InlineKeyboardButton("تقسیم مساوی بین همه", callback_data="0"),
        InlineKeyboardButton("تقسیم مساوی بین بعضی از افراد", callback_data="1"),
        InlineKeyboardButton("تقسیم دلحواه", callback_data="2")
    ]
    n_cols = 1
    menu = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
    reply_markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(id, "نوع پرداخت هزینه را انتخاب کنید", reply_markup=reply_markup)
