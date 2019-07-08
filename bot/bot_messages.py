import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Message
from emoji import emojize
from bot.bot_functions import MarketType, market_type_names


def send_message_send_cost(bot, id):
    try:
        bot.sendMessage(id, "لطفا مقدار هزینه را وارد کنید")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_command_not_found(bot, id):
    bot.sendMessage(id, "هنو این کامندو اضافه نکردیم!")


def send_message_already_registered(bot, id):
    try:
        bot.sendMessage(id, emojize("you have already registered sir! :man_in_tuxedo: :kiss:", use_aliases=True))
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_private_chat(bot, id):
    try:
        bot.sendMessage(id, "من با تو صحبتی ندارم.")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_have_not_selected_users(bot, id):
    try:
        bot.sendMessage(id, "دِ خب یکیو انتخاب کن!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_canceled(bot, id):
    try:
        bot.sendMessage(id, "کنسله!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_remaining(bot, id, value):
    try:
        bot.sendMessage(id, "مقدار " + str(value) + " باقیمانده برای خود شما ثبت شد.")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_send_every_user_share(bot, id):
    try:
        bot.sendMessage(id, "هر کدوم چقد پول دادن؟")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_get_name(bot, id):
    try:
        bot.sendMessage(id, "چیکار کردی با این پول؟")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_mydebt(bot, id, result):
    try:
        if result > 0:
            bot.sendMessage(id, emojize("شما %d دلار بدهکار هستید :sunglasses:" % result, use_aliases=True))
        else:
            bot.sendMessage(id, emojize(" شما %d دلار طلبکار هستید :sunglasses: " % (-1 * result), use_aliases=True))
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_username(bot, id, username):
    try:
        bot.sendMessage(id, "" + username + " :")  # can add @ at first
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_user_registered(bot, id):
    try:
        bot.sendMessage(id, emojize("ای بابا تو رو کی راه داده؟! :man_facepalming:", use_aliases=True))
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_share_exceeded(bot, id):
    try:
        bot.sendMessage(id, "اینکه بیشتر از اون پولی که گفتی شد!\n برو خودتو اسکل کن")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_reply_without_state_error(bot, id):
    try:
        bot.sendMessage(id, "مگه من مسخره توام!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_not_a_number_error(bot, id):
    try:
        bot.sendMessage(id, "ببین چگونه جان مشوش است عدد بده!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_not_a_message(bot, id):
    try:
        bot.sendMessage(id, "دکمه نزن بچه!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_not_a_callback(bot, id):
    try:
        bot.sendMessage(id, "دکمه بزن!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_cache_not_found(bot, id):
    try:
        bot.sendMessage(id, "برو بگو خودش بیاد!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_have_not_members(bot, id):
    try:
        bot.sendMessage(id, "هیچ کدام از شما لاشیا ثبت نام نکردید!")
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_added_cost(bot, id):
    try:
        bot.sendMessage(id, emojize("باتشکر :rose: :rose:", use_aliases=True))
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_select_cost_kind(bot, id):
    try:
        button_list = [
            InlineKeyboardButton("تقسیم مساوی بین همه", callback_data="0"),
            InlineKeyboardButton("تقسیم مساوی بین بعضی از افراد", callback_data="1"),
            InlineKeyboardButton("تقسیم دلخواه", callback_data="2")
        ]
        n_cols = 1
        menu = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
        reply_markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(id, "نوع پرداخت هزینه را انتخاب کنید", reply_markup=reply_markup)
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_select_users(bot, id, users, selecteds, message_id=None):
    try:
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
            bot.edit_message_reply_markup(id, message_id, reply_markup=reply_markup)
    except telegram.error.BadRequest:
        print("error: telegram bad request")


def send_message_getalldebts(bot, id, payement):
    res = ''
    for pay in payement:
        res += str(pay[2]) + " :  " + pay[0] + ' --> ' + pay[1] + '\n'

    bot.sendMessage(id, res)


def send_message_select_type(bot, id):
    button_list = []
    for type in MarketType:
        try:
            button_text = market_type_names[type.value[0]]
            button_list.append(
                InlineKeyboardButton(emojize(button_text, use_aliases=True), callback_data=str(type.value[0])))
        except Exception as e:
            print(e)
    n_cols = 1
    menu = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
    reply_markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(id, "چی داری؟", reply_markup=reply_markup)


def send_message_send_name(bot, id):
    bot.sendMessage(id, "اسمت چیه عمو؟")


def send_message_send_desc(bot, id):
    bot.sendMessage(id, "توضیح بده!")


def send_message_market_saved(bot, id):
    bot.sendMessage(id, "محل به بات افزوده شد.")
