import argparse
from collections import defaultdict
from aiogram import Bot, types
import tracemalloc

import pandas as pd
from src.single_bot.Geter import get_media
from src.single_bot.config import TOKEN
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher


fl = defaultdict(int)
answ = defaultdict(int)
n_of_pics = defaultdict(int)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def GenPic(msg: types.Message):
    global answ, fl
    fl[msg.chat.id] = 0
    await msg.reply("Сейчас ты получишь картинки и должен сказать, какая была сгенерирована нейросетью изначально",
                    reply_markup=types.ReplyKeyboardRemove())

    media_r, answ[msg.chat.id], text, n_of_pics[msg.chat.id] = get_media(base)
    buttons = [str(i + 1) for i in range(n_of_pics[msg.chat.id])]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    print(f"Media generated for user {msg.chat.id}")
    await bot.send_media_group(msg.chat.id, media=media_r)
    await msg.answer(
        'Картинка была сгенерирована по тексту: "' + text + '". Какой ответ?',
        reply_markup=keyboard)


async def GetAns(msg: types.Message):
    global answ, fl

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    if msg.text == str(answ[msg.chat.id]):
        await msg.reply(
            f"Да, правильный ответ {answ[msg.chat.id]}! Играем еще?",
            reply_markup=keyboard)
    else:
        await msg.reply(
            f"Очень жаль, но {msg.text} это неправильный ответ. Правильный ответ {answ[msg.chat.id]}. Играем еще?",
            reply_markup=keyboard)
    answ[msg.chat.id] = -1
    fl[msg.chat.id] = 1


async def Finish(msg: types.Message):
    global fl
    fl[msg.chat.id] = 0
    await msg.reply("Если захочешь поиграть еще, напиши /start", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    global fl, answ
    
    fl[msg.chat.id] = 1
    answ[msg.chat.id] = -1
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    print("Bot started")
    await msg.answer(
        "Привет. Я Imagen imaginarium bot. Со мной ты можешь играть в imaginarium, где картинки будут сгенерированы нейросетью. Начинаем?",
        reply_markup=keyboard)


@dp.message_handler()
async def Main(msg: types.Message):
    if fl[msg.chat.id] and msg.text == "Да!":
        print(f"GenPic for user {msg.chat.id}")
        await GenPic(msg)
    elif answ[msg.chat.id] != -1 and msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= n_of_pics[msg.chat.id]:
        print(f"GenAns for user {msg.chat.id}")
        await GetAns(msg)
    if msg.text == "Хватит":
        print(f"Finish for user {msg.chat.id}")
        await Finish(msg)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--images_path', type=str, default='Images',
                        help='where images are stored')
    parser.add_argument('--database_name', type=str, default='Database.csv',
                        help='where database is stored')

    args = parser.parse_args()
    base = pd.read_csv(args.database_name)

    print("polling")
    executor.start_polling(dp, skip_updates=True)
