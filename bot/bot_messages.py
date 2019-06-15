import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Message
from emoji import emojize


def send_message_send_cost(bot, id):
    bot.sendMessage(id, "لطفا مقدار هزینه را وارد کنید")


def send_message_already_registered(bot, id):
    bot.sendMessage(id, emojize("you have already registered sir! :man_in_tuxedo: :kiss:", use_aliases=True))


def send_message_private_chat(bot, id):
    bot.sendMessage(id, "من با تو صحبتی ندارم.")


def send_message_have_not_selected_users(bot, id):
    bot.sendMessage(id, "دِ خب یکیو انتخاب کن!")


def send_message_canceled(bot, id):
    bot.sendMessage(id, "کنسله!")


def send_message_remaining(bot, id, value):
    bot.sendMessage(id, "مقدار " + str(value) + " باقیمانده برای خود شما ثبت شد.")


def send_message_send_every_user_share(bot, id):
    bot.sendMessage(id, "هر کدوم چقد پول دادن؟")


def send_message_get_name(bot, id):
    bot.sendMessage(id, "چیکار کردی با این پول؟")


def send_message_mydebt(bot, id, result):
    if result > 0:
        bot.sendMessage(id, emojize("شما %d دلار بدهکار هستید :sunglasses:" % result, use_aliases=True))
    else:
        bot.sendMessage(id, emojize(" شما %d دلار طلبکار هستید :sunglasses: " % (-1 * result), use_aliases=True))


def send_message_username(bot, id, username):
    bot.sendMessage(id, "" + username + " :")  # can add @ at first


def send_message_user_registered(bot, id):
    bot.sendMessage(id, emojize("ای بابا تو رو کی راه داده؟! :man_facepalming:", use_aliases=True))


def send_message_share_exceeded(bot, id):
    bot.sendMessage(id, "اینکه بیشتر از اون پولی که گفتی شد!\n برو خودتو اسکل کن")


def send_message_reply_without_state_error(bot, id):
    bot.sendMessage(id, "مگه من مسخره توام!")


Bot,


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
        InlineKeyboardButton("تقسیم دلخواه", callback_data="2")
    ]
    n_cols = 1
    menu = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
    reply_markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(id, "نوع پرداخت هزینه را انتخاب کنید", reply_markup=reply_markup)


def send_message_select_users(bot, id, users, selecteds, message_id=None):
    button_list = []
    for user in users:
        button_text = user.username
        if str(user.id) in selecteds:
            button_text += " - :white_check_mark: "
        button_list.append(InlineKeyboardButton(emojize(button_text, use_aliases=True), callback_data=user.id))
    button_list.append(InlineKeyboardButton("همینا بودن", callback_data="ended"))
    n_cols = 2
    menu = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
    reply_markup = InlineKeyboardMarkup(menu)
    if message_id is None:
        message = bot.sendMessage(id, "کدومشون بود؟", reply_markup=reply_markup)
        return message.message_id
    else:
        try:
            bot.edit_message_reply_markup(id, message_id, reply_markup=reply_markup)
        except telegram.error.BadRequest:
            return


def send_message_getalldebts(bot, id, payement):
    res = ''
    for pay in payement:
        res += str(pay[2]) + " :  " + pay[0] + ' --> ' + pay[1] + '\n'

    bot.sendMessage(id, res)
