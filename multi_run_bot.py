import argparse
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pandas as pd

from src.multi_bot.config import TOKEN
from src.multi_bot import Geter
from src.multi_bot.gen_photo import shuffle

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

Gamers = {}
list_keys = {}

async def AddMe(msg : types.Message):
    if msg.text not in list_keys:
        list_keys[msg.text] = Geter.Game(base)
    elif list_keys[msg.text].isStart:
        await msg.reply("Игра с таким ключом уже началась. Используйте другой ключ.")
        return
 
    Game = list_keys[msg.text]
    Gamers[msg.chat.id] = Game
    Game.add_RealGamer(msg.chat.id, msg.chat.username, Game)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    if len(Game.List) <= 2:
        buttons = ["Да"]
    keyboard.add(*buttons)
    Gamers[msg.chat.id].fl = 2
    await msg.reply("Сейчас вас " + str(len(Game.List)) + ". Ждем еще?",
                    reply_markup=keyboard)

async def Finish(id : int):
    global list_keys, Gamers

    cur_Game = Gamers[id]
    del Gamers[id]
    if cur_Game not in Gamers.values():
        list_keys.remove(cur_Game)
    
    await bot.send_message(id, "Если захочешь поиграть еще, напиши /start", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # buttons = ["Да!", "Хватит"]
    # keyboard.add(*buttons)

    if msg.chat.id in Gamers:
        if msg.chat.id in Gamers[msg.chat.id].List:
            Gamers[msg.chat.id].List.remove(msg.chat.id)
        del Gamers[msg.chat.id]

    await msg.answer(
"""
Привет!
Я 💫Imagen Imaginarium bot💫
Со мной ты можешь играть в Imaginarium, где картинки будут сгенерированы нейросетью.
Чтобы начать пришли мне существующий ключ комнаты или придумай свой (любая строка) и сообщи его друзьям.
"""
)

@dp.message_handler()
async def Main(msg: types.Message):
    f = 0
    if not msg.chat.id in Gamers:
        f = 1
    if f:
        await AddMe(msg)
        return
    if not msg.chat.id in Gamers:
        return
    Game = Gamers[msg.chat.id]
    print(msg.chat.id, msg.text, Game.fl, Game.List)
    if (msg.text == "Да" and Game.fl == 2) or len(Game.List) < 3:
        await msg.answer(f"Всего ожидающих в вашей комнате: {len(Game.List)}.\nЕсли захотите начать игру напишите мне 'Нет'.\nЧтобы узнать актуальное количество ожидающих пришлите мне любое сообщение кроме 'Нет'.", reply_markup=types.ReplyKeyboardRemove())
    if (msg.text == "Нет" and Game.fl == 2) or (Game.fl == 3 and msg.text == "Да!"):
        for u in Game.List:
            await bot.send_message(u.id, "Начинаем", reply_markup=types.ReplyKeyboardRemove())
        Game.start()
        Game.fl = 0
        Game.ff3 = 1
    Game.go()

    if Game.stage_id == 0:
        Game.ff = Game.ff2 = 1
        if not Game.ff3 and msg.chat.id == Game.List[Game.lead].id and \
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
        elif Game.ff3:
            Game.ff3 = 0
            for u in Game.List:
                if u.id != Game.List[Game.lead].id:
                    await bot.send_message(u.id, "Ждем ведущего... (@" + Game.List[Game.lead].name + ')')
            await bot.send_media_group(Game.List[Game.lead].id, media=Game.Gamers[Game.List[Game.lead].id].MedGroup)
            await bot.send_message(Game.List[Game.lead].id,
                                       "Ты - ведущий. Отправь сообщение с номером картинки и комментарием к ней через пробел")
        return
    Game.go()

    if Game.stage_id == 1:
        if msg.chat.id != Game.List[Game.lead].id:
            if msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= len(Game.Gamers[msg.chat.id].MedGroup.media):
                Game.Gamers[msg.chat.id].set_imag(int(msg.text), "-")
                await msg.answer("Серьезно? " + msg.text + "? Как знаешь...")
        else:
            await msg.answer("Жди, ведущий")

    Game.go()

    if Game.stage_id == 2:
        if Game.ff:
            Game.ff = 0
            for u in Game.List:
                await bot.send_message(u.id, "Наконец-то все что-то выбрали. Ура", reply_markup=types.ReplyKeyboardRemove())

                await bot.send_media_group(u.id, media=Game.all_map())
                if u.id != Game.List[Game.lead].id:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons = []
                    for i in range(len(Game.List)):
                        buttons.append(str(i + 1))
                    keyboard.add(*buttons)
                    await bot.send_message(u.id, "Угадай карточку, которую ведущий загадал как:\n"+Game.List[
                                               Game.lead].text, reply_markup=keyboard)
        elif msg.chat.id != Game.List[Game.lead].id and msg.text.isdigit() and int(msg.text) >= 1 and int(msg.text) <= len(Game.List):
            Game.Gamers[msg.chat.id].ans = int(msg.text) - 1
            await msg.answer("Ок, ты выбрал картинку " + msg.text)
    Game.go()

    if Game.stage_id == 3:
        if Game.ff2:
            Game.ff2 = 0
            for u in Game.List:
                await bot.send_message(u.id, Game.get_leader_board(), reply_markup=types.ReplyKeyboardRemove())
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да!", "Хватит"]
            keyboard.add(*buttons)
            await bot.send_message(Game.get_lead_id(), "Играем еще?", reply_markup=keyboard)
            Game.fl = 3
        elif msg.text == "Хватит":
            for u in Game.List:
                await Finish(u.id)
            Game.fl = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--images_path', type=str, default='Images',
                        help='where images are stored')
    parser.add_argument('--database_name', type=str, default='Database.csv',
                        help='where database is stored')

    args = parser.parse_args()
    base = pd.read_csv(args.database_name)
    base = shuffle(base)

    print("polling")
    executor.start_polling(dp, skip_updates=True)