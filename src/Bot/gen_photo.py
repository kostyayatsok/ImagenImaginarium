from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pymorphy2

t = 0
def get_photo():
    global t
    s = "C:/Users/Dan/Pictures/img/" + str(t) + ".jpg"
    t = (t + 1) % 20
    return s
