from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import copy
import re
from config import TOKEN
import Geter

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ff = 0
ff2 = 0

Game = Geter.Game()

async def AddMe(msg : types.Message):
    Game.add_RealGamer(msg.chat.id, msg.chat.first_name)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    if len(Game.List) <= 2:
        buttons = ["Да"]
    keyboard.add(*buttons)
    await msg.reply("Сейчас вас " + str(len(Game.List)) + ". Ждем еще?",
                    reply_markup=keyboard)

async def Finish(id : int):
    global Game
    Game = Geter.Game()
    await bot.send_message(id, "Если захочешь поиграть еще, напиши /start", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да!", "Хватит"]
    keyboard.add(*buttons)
    await msg.answer(
        "Привет. Я Imagen imaginarium bot. Со мной ты можешь играть в imaginarium, где картинки будут сгенерированы нейросетью. Начинаем?",
        reply_markup=keyboard)

@dp.message_handler()
async def Main(msg: types.Message):
    global ff, ff2
    if not msg.chat.id in Game.Gamers and msg.text == "Да!":
        await AddMe(msg)
        Game.fl = 2
        return
    if msg.text == "Да" and Game.fl == 2:
        await msg.answer("Ну и жди", reply_markup=types.ReplyKeyboardRemove())
        Game.fl = 0
    if msg.text == "Нет" and Game.fl == 2:
        for u in Game.List:
            await bot.send_message(u.id, "Начинаем", reply_markup=types.ReplyKeyboardRemove())
        Game.start()
        Game.fl = 0


    Game.go()

    if Game.stage_id == 0:
        ff = ff2 = 1
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
            for u in Game.List:
                if u.id != Game.List[Game.lead].id:
                    await bot.send_message(u.id, "Ждем ведущего...")
            await bot.send_media_group(Game.List[Game.lead].id, media=Game.Gamers[Game.List[Game.lead].id].MedGroup)
            await bot.send_message(Game.List[Game.lead].id,
                                       "Ты - ведущий. Отправь сообщение с номером картинки и комментарием к ней через пробел")
        return
    Game.go()

    if Game.stage_id == 1:
        if msg.chat.id != Game.List[Game.lead].id:
            if msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= len(Game.Gamers[msg.chat.id].MedGroup.media):
                Game.Gamers[msg.chat.id].set_imag(int(msg.text), "-")
        else:
            await msg.answer("Жди")

    Game.go()

    if Game.stage_id == 2:
        if ff:
            ff = 0
            for u in Game.List:
                await bot.send_message(u.id, "Наконец-то все что-то выбрали. Ура", reply_markup=types.ReplyKeyboardRemove())

                await bot.send_media_group(u.id, media=Game.all_map())
                if u.id != Game.List[Game.lead].id:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons = []
                    for i in range(len(Game.List)):
                        buttons.append(str(i + 1))
                    keyboard.add(*buttons)
                    await bot.send_message(u.id, "Выбирай правильный ответ...", reply_markup=keyboard)
        elif msg.chat.id != Game.List[Game.lead].id and msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= len(Game.List):
            Game.Gamers[msg.chat.id].ans = int(msg.text) - 1
    Game.go()

    if Game.stage_id == 3:
        if ff2:
            ff2 = 0
            for u in Game.List:
                await bot.send_message(u.id, Game.get_leader_board(), reply_markup=types.ReplyKeyboardRemove())
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = ["Да!", "Хватит"]
                keyboard.add(*buttons)
                await bot.send_message(u.id, "Играем еще?", reply_markup=keyboard)
        else:
            if msg.text == "Хватит":
                for u in Game.List:
                    await Finish(u.id)
            else:
                for u in Game.List:
                    await bot.send_message(u.id, "Продолжаем (напишите что-нибудь)", reply_markup=types.ReplyKeyboardRemove())
                Game.start()


if __name__ == '__main__':
    executor.start_polling(dp)