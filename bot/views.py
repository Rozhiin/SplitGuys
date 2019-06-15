from django.http import HttpResponse
import telegram
from bot import json_parser
from bot.bot_main import handle_update
import json


def hello(request):
    try:
        bot = telegram.Bot("876650276:AAEWj4fDYthgU4MFPIKJT7H5WUxKnbep1mY")
        update_json = json.loads(request.body)
        update = json_parser.make_update_from_json(update_json)
        handle_update(bot, update)
    except telegram.error.BadRequest:
        print("ERROR")
    return HttpResponse("hello3")
