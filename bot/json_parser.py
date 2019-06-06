from telegram import Update, Message, User, Chat, CallbackQuery


def make_chat_from_json(chat_json):
    chat = Chat(chat_json['id'], chat_json['type'])
    return chat


def make_user_from_json(user_json):
    user = User(user_json['id'], user_json['first_name'], user_json['is_bot'],
                username=user_json['username'])
    return user


def make_message_from_json(message_json):
    message = Message(message_json['message_id'],
                      from_user=make_user_from_json(message_json['from']),
                      date=message_json['date'],
                      chat=make_chat_from_json(message_json['chat']),
                      text=message_json['text'])
    return message


def make_callback_query_from_json(callback_json):
    callback_query = CallbackQuery(callback_json['id'],
                                   from_user=make_user_from_json(callback_json['from']),
                                   message=make_message_from_json(callback_json['message']),
                                   chat_instance=callback_json['chat_instance'],
                                   data=callback_json['data'])
    return callback_query


def make_update_from_json(update_json):
    if not 'update_id' in update_json:
        return None
    update = Update(update_json['update_id'])
    if 'callback_query' in update_json:
        update.callback_query = make_callback_query_from_json(update_json['callback_query'])
    elif 'message' in update_json:
        update.message = make_message_from_json(update_json['message'])
    return update
