from aiogram import Bot, types
import tracemalloc
from src.single_bot.Geter import get_media
from src.single_bot.config import TOKEN
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

tracemalloc.start()

fl = 0
answ = -1
gamers = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def GenPic(msg: types.Message):
    global answ, fl
    fl = 0
    await msg.reply("Сейчас ты получишь 5 картинок и должен сказать, какая была сгенерирована нейросетью изначально",
                    reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1", "2", "3", "4", "5"]
    keyboard.add(*buttons)
    media_r, answ, text = get_media()
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
    if msg.text == str(answ):
        await msg.reply(
            f"Да, правильный ответ {answ}! Играем еще?",
            reply_markup=keyboard)
    else:
        await msg.reply(
            f"Очень жаль, но {msg.text} это неправильный ответ. Правильный ответ {answ}. Играем еще?",
            reply_markup=keyboard)
    answ = -1
    fl = 1


async def Finish(msg: types.Message):
    await msg.reply("Если захочешь поиграть еще, напиши /start", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    global fl
    fl = 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    print("Bot started")
    await msg.answer(
        "Привет. Я Imagen imaginarium bot. Со мной ты можешь играть в imaginarium, где картинки будут сгенерированы нейросетью. Начинаем?",
        reply_markup=keyboard)


@dp.message_handler()
async def Main(msg: types.Message):
    if fl and msg.text == "Да!":
        print(f"GenPic for user {msg.chat.id}")
        await GenPic(msg)
    elif answ != -1 and msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= 5:
        print(f"GenAns for user {msg.chat.id}")
        await GetAns(msg)
    if msg.text == "Хватит":
        print(f"Finish for user {msg.chat.id}")
        await Finish(msg)

if __name__ == '__main__':
    print("polling")
    executor.start_polling(dp, skip_updates=True)
