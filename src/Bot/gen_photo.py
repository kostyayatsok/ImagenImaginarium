from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pymorphy2

def get_photo():
    return types.InputFile('C:/Users/Dan/Pictures/img.png')