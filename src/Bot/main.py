from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import re
from config import TOKEN
import Geter

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

fl = 0
answ = -1

Game = Geter.Game()

async def AddMe(msg : types.Message):
    Game.add_RealGamer(msg.chat.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    #if len(Game.List) == 2:
    #    buttons = ["Да", "Да"]
    keyboard.add(*buttons)
    await msg.reply("Сейчас вас " + str(len(Game.List)) + ". Ждем еще?",
                    reply_markup=keyboard)

'''
async def GenPic(msg: types.Message):
    global answ, fl
    fl = 0
    await msg.reply("Сейчас ты получишь несколько картинок и должен сказать, какая была выбрана лидером изначально",
                    reply_markup=types.ReplyKeyboardRemove())

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
'''

async def Finish(msg : types.Message):
    await msg.reply("Если захочешь поиграть еще, напиши /start", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    global fl
    fl = 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    await msg.answer(
        "Привет. Я Imagen imaginarium bot. Со мной ты можешь играть в imaginarium, где картинки будут сгенерированы нейросетью. Начинаем?",
        reply_markup=keyboard)

@dp.message_handler()
async def Main(msg: types.Message):
    global fl
    if fl == 1 and msg.text == "Да!":
        await AddMe(msg)
        fl = 2
        return
    if msg.text == "Нет" and fl == 2:
        for u in Game.List:
            await bot.send_message(u.id, "Начинаем", reply_markup=types.ReplyKeyboardRemove())
        Game.start()
        fl = 0
    Game.go()
    if Game.stage_id == 0:
        if msg.chat.id == Game.List[Game.lead].id and \
                msg.text[0].isdigit() and int(msg.text[0]) >= 1 and int(msg.text[0]) <= len(Game.List[Game.lead].MedGroup.media):
            Game.Gamers[msg.chat.id].set_imag(int(msg.text[0]), msg.text[2:])
            await msg.answer("Так и запишем")

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["1", "2", "3", "4", "5", "6"]
            keyboard.add(*buttons)

            for u in Game.List:
                if u.id != Game.List[Game.lead].id:
                    await bot.send_media_group(u.id, media=Game.Gamers[u.id].MedGroup)
                    await bot.send_message(u.id,
                                           'Ведущий выбрал картинку. Теперь выбери картинку по ассоциации: "' + Game.List[
                                               Game.lead].text + '"'
                                           , reply_markup=keyboard)
        else:
            await bot.send_media_group(Game.List[Game.lead].id, media=Game.Gamers[Game.List[Game.lead].id].MedGroup)
            await bot.send_message(Game.List[Game.lead].id, "Ты - ведущий. Отправь сообщение с номером картинки и комментарием к ней через пробел")
            if msg.chat.id != Game.List[Game.lead].id:
                await msg.answer("Ждем ведущего...")
        return

    if Game.stage_id == 1:
        if msg.chat.id != Game.List[Game.lead].id:
            if msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= len(Game.Gamers[msg.chat.id].MedGroup.media):
                Game.Gamers[msg.chat.id].set_imag(int(msg.text), "-")
        else:
            await msg.answer("Жди")
    Game.go()
    if Game.stage_id == 2:
        for u in Game.List:
            await bot.send_message(u.id, "Наконец-то все что-то выбрали. Ура", reply_markup=types.ReplyKeyboardRemove())
            await bot.send_media_group(u.id, media=Game.all_map)
            if u.id != Game.List[Game.lead].id:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = []
                for i in range(len(Game.List)):
                    buttons.append(str(i + 1))
                keyboard.add(*buttons)
                await bot.send_message(u.id, "Выбирай правильный ответ...", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)