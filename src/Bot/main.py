from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pymorphy2
import tracemalloc

tracemalloc.start()

import re
morph = pymorphy2.MorphAnalyzer()

from config import TOKEN
from Geter import get_media

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

fl = 0
answ = -1
gamers = {}

async def GenPic(msg: types.Message):
    global answ, fl
    fl = 0
    await msg.reply("Сейчас ты получишь 5 картинок и должен сказать, какая была сгенерирована нейросетью изначально", reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1", "2", "3", "4", "5"]
    keyboard.add(*buttons)
    data = get_media()
    answ = data[1]
    await bot.send_media_group(msg.chat.id, media=data[0])
    await msg.answer(
        'Картинка была сгенерирована по тексту: "' + data[2] + '". Какой ответ?',
        reply_markup=keyboard)

async def GetAns(msg: types.Message):
    global answ, fl
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    if msg.text == str(answ):
        await msg.reply(
            "Правильно! Играем еще?",
            reply_markup=keyboard)
    else:
        await msg.reply(
            "Очень жаль. Неправильно(. Играем еще?",
            reply_markup=keyboard)
    answ = -1
    fl = 1

async def Finish(msg : types.Message):
    await msg.reply("Если захочешь поиграть еще, напиши /start", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    global fl
    fl = 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    await msg.answer("Привет. Я Imagen imaginarium bot. Со мной ты можешь играть в imaginarium, где картинки будут сгенерированы нейросетью. Начинаем?", reply_markup=keyboard)

@dp.message_handler()
async def Main(msg: types.Message):
    if fl and msg.text == "Да!":
        await GenPic(msg)
    elif answ != -1 and msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= 5:
        await GetAns(msg)
    if msg.text == "Хватит":
        await Finish(msg)

if __name__ == '__main__':
    executor.start_polling(dp)