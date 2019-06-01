from django.http import HttpResponse
from django.shortcuts import render
import telepot


# Create your views here.
def hello(request):
    bot = telepot.Bot("876650276:AAEWj4fDYthgU4MFPIKJT7H5WUxKnbep1mY")
    content_type, chat_type, chat_id = telepot.glance(request)
    print("this is id ", request.body)
    bot.sendMessage(104342320, content_type)
    return HttpResponse("hell", request.body)
