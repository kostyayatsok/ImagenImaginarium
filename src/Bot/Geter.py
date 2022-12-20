from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from src/Bot/gen_photo import *
import random
import copy


class RealGamer:
    def __init__(self, my_id : int, my_name : str):
        self.score = 0
        self.MedGroup = types.MediaGroup()
        self.MG = list()
        self.media_id = -1
        self.ans = -1
        self.name = my_name
        for i in range(6):
            self.MG.append(get_photo())
            self.MedGroup.attach_photo(types.InputFile(self.MG[i]))
        self.id = my_id
        self.text = "Первая картинка - правильная"
    def get_media(self): #загаданный текст и число картинки
        return [self.MedGroup[self.media_id], self.text]
    def set_imag(self, k : int, tx : str): #Изменение текста и числа
        # global media_id, text
        self.media_id = k
        self.text = tx
    def upd_media(self):
        self.MG[self.media_id - 1] = get_photo()
        self.MedGroup = types.MediaGroup()
        for i in self.MG:
           self.MedGroup.attach_photo(types.InputFile(i))
        self.media_id = -1
        self.ans = -1

class Game:
    def __init__(self):
        self.Gamers = {}
        self.List = list()
        self.lead = -1
        self.stage_id = -1
        self.all_map2 = list()
        self.id_to_map = list()

    def add_RealGamer(self, user_id : int, name : str):
        self.Gamers[user_id] = RealGamer(user_id, name)
        self.List.append(self.Gamers[user_id])

    def start(self):
        self.id_to_map = list()
        self.lead = (self.lead + 1) % len(self.List)
        self.stage_id = 0
        for u in self.List:
            u.upd_media()

    def upd_score(self):
        fl2 = 1
        fl3 = 1
        for u in self.List:
            if u.id != self.get_lead_id() and self.id_to_map[u.ans] != self.get_lead_id():
                fl2 = 0
            if u.id != self.get_lead_id() and self.id_to_map[u.ans] == self.get_lead_id():
                fl3 = 0
        if fl2 or fl3:
            for u in self.List:
                if u.id != self.get_lead_id():
                    u.score += 2
            return
        self.List[self.lead].score += 3
        for u in self.List:
            if u.id != self.get_lead_id():
                if self.id_to_map[u.ans] == self.get_lead_id():
                    u.score += 3
                else:
                    self.Gamers[self.id_to_map[u.ans]].score += 1

    def go(self):
        if self.List[self.lead].media_id != -1 and self.stage_id == 0:
            self.stage_id = 1
            return
        fl = 1
        for u in self.List:
            if u.media_id == -1:
                fl = 0
        if self.stage_id == 1 and fl:
            self.all_map2 = list()
            self.id_to_map = list()
            for u in self.List:
                self.all_map2.append(u.MG[u.media_id - 1])
                self.id_to_map.append(u.id)

            for i in range(len(self.List)):
                to_swap = random.randrange(i + 1)
                self.all_map2[i], self.all_map2[to_swap] = self.all_map2[to_swap], self.all_map2[i]
                self.id_to_map[i], self.id_to_map[to_swap] = self.id_to_map[to_swap], self.id_to_map[i]

            self.stage_id = 2
            return

        fl = 1
        for u in self.List:
            if u.id != self.get_lead_id() and u.ans == -1:
                fl = 0
        if self.stage_id == 2 and fl:
            self.stage_id = 3
            self.upd_score()

    def all_map(self):
        all = types.MediaGroup()
        for u in self.all_map2:
            all.attach_photo(types.InputFile(u))
        return all

    def get_lead_id(self):
        return self.List[self.lead].id

    def get_leader_board(self):
        text = "Очки:\n"
        for u in self.List:
            text += str(u.name) + ' : ' + str(u.score) + '\n'
        return text

