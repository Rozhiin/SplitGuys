from django.http import HttpResponse
from django.shortcuts import render
import telepot


# Create your views here.
def hello(request):
    bot = telepot.Bot("876650276:AAEWj4fDYthgU4MFPIKJT7H5WUxKnbep1mY")
    bot.sendMessage(104342322, "hello from django")
    return HttpResponse("hello")
