from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from gen_photo import *
import random

class Gamer:
    def get_media(self):
        pass

class RealGamer(Gamer):
    # text = ""
    # score = 0
    # id = 0
    # MedGroup = types.MediaGroup()
    # media_id = -1
    # ans = -1
    def __init__(self, my_id : int):
        self.score = 0
        self.MedGroup = types.MediaGroup()
        self.MG = list()
        self.media_id = -1
        self.ans = -1
        # global id, text, MedGroup
        for i in range(6):
            self.MG.append(get_photo())
            self.MedGroup.attach_photo(self.MG[i])
        self.id = my_id
        self.text = "Первая картинка - правильная"
    def get_media(self): #загаданный текст и число картинки
        return [self.MedGroup[self.media_id], self.text]
    def set_imag(self, k : int, tx : str): #Изменение текста и числа
        # global media_id, text
        self.media_id = k
        self.text = tx
    def upd_media(self):
        self.MG[self.media_id] = get_photo()
        self.MedGroup.clean()
        for i in self.MG:
           self.MedGroup.attach_photo(i)
        self.media_id = -1
        self.ans = -1


class BotGamer(Gamer):
    def get_media(self):
        media = types.MediaGroup()
        for i in range(5):
            media.attach_photo(types.InputFile('C:/Users/Dan/Pictures/img.png'))
        text = "Первая картинка - правильная"
        return [media, 1, text]

class Game:
    def __init__(self):
        self.Gamers = {}
        self.List = list()
        self.lead = -1
        self.stage = ["Ведущий выбирает карту", "Игроки выбирают ассоциацию", "Игроки выбирают оригинальную карту"]
        self.stage_id = -1

        self.all_map = types.MediaGroup()
        self.id_to_map = list()

    def add_RealGamer(self, user_id : int):
        self.Gamers[user_id] = RealGamer(user_id)
        self.List.append(self.Gamers[user_id])

    def start(self):
        self.all_map.media.clear()
        self.id_to_map.clear()
        self.lead = (self.lead + 1) % len(self.List)
        self.stage_id = 0

    def go(self):
        if self.List[self.lead].media_id != -1 and self.stage_id == 0:
            self.stage_id = 1
        fl = 1
        for u in self.List:
            if u.media_id == -1:
                fl = 0
        if self.stage_id == 1 and fl and len(self.all_map.media) == 0:
            all_map2 = list()
            for u in self.List:
                all_map2.append(u.MG[u.media_id])
                self.id_to_map.append(u.id)

            for i in range(len(self.List)):
                to_swap = random.randrange(i + 1)
                all_map2[i], all_map2[to_swap] = all_map2[to_swap], all_map2[i]
                self.id_to_map[i], self.id_to_map[to_swap] = self.id_to_map[to_swap], self.id_to_map[i]

            self.all_map.clean()
            for u in all_map2:
                self.all_map.attach_photo(u)
            self.stage_id = 2
            return
        fl = 1
        for u in self.List:
            if u.ans == -1:
                fl = 0
        if self.stage_id == 2 and fl: #пока неправильный подсчет очков
            for u in self.List:
                self.Gamers[self.id_to_map[u.ans]].score += 1

    def get_lead_id(self):
        return self.List[self.lead].id

    def get_leader_board(self):
        text = ""
        for u in self.List:
            text += str(u.id) + ' : ' + str(u.score) + '\n'
        return text

