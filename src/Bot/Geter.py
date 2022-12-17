from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pymorphy2

def get_media():
    media = types.MediaGroup()
    for i in range(5):
        media.attach_photo(types.InputFile('C:/Users/Dan/Pictures/img.png'))
    text = "Первая картинка - правильная"
    return [media, 1, text]