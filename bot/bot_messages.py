from  telegram import InlineKeyboardButton, InlineKeyboardMarkup


def send_message_send_cost(bot, id):
    bot.sendMessage(id, "لطفا مقدار هزینه را وارد کنید")


def send_message_reply_without_state_error(bot, id):
    bot.sendMessage(id, "مگه من مسخره توام!")


def send_message_not_a_number_error(bot, id):
    bot.sendMessage(id, "ببین چگونه جان مشوش است عدد بده!")


def send_message_select_cost_kind(bot, id):
    button_list = [
        InlineKeyboardButton("تقسیم مساوی بین همه", callback_data="0"),
        InlineKeyboardButton("تقسیم مساوی بین بعضی از افراد", callback_data="1"),
        InlineKeyboardButton("تقسیم دلحواه", callback_data="2")
    ]
    n_cols = 3
    menu = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
    reply_markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(id, "نوع پرداخت هزینه را انتخاب کنید", reply_markup=reply_markup)