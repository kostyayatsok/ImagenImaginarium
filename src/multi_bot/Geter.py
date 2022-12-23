from aiogram import types
from src.multi_bot.gen_photo import *
import random


class RealGamer:
    def __init__(self, my_id : int, my_name : str, mGame, base):
        self.score = 0
        self.MedGroup = types.MediaGroup()
        self.MG = list()
        self.media_id = -1
        self.ans = -1
        self.name = my_name
        self.my_Game = mGame
        for i in range(6):
            gp, self.my_Game.t = get_photo(base, self.my_Game.t)
            self.MG.append(gp)
            self.MedGroup.attach_photo(types.InputFile(self.MG[i]))
        self.id = my_id
        self.text = "Первая картинка - правильная"
        self.base = base
    def get_media(self): #загаданный текст и число картинки
        return [self.MedGroup[self.media_id], self.text]
    def set_imag(self, k : int, tx : str): #Изменение текста и числа
        # global media_id, text
        self.media_id = k
        self.text = tx
    def upd_media(self):
        gp, self.my_Game.t = get_photo(self.base, self.my_Game.t)
        self.MG[self.media_id - 1] = gp
        self.MedGroup = types.MediaGroup()
        for i in self.MG:
           self.MedGroup.attach_photo(types.InputFile(i))
        self.media_id = -1
        self.ans = -1

class Game:
    def __init__(self, base):
        self.Gamers = {}
        self.List = list()
        self.lead = -1
        self.stage_id = -1
        self.fl = 0
        self.all_map2 = list()
        self.id_to_map = list()
        self.isStart = 0
        self.ff = 0
        self.ff2 = 0
        self.ff3 = 0
        self.t = 0
        shuffle(base)
        self.base = base

    def add_RealGamer(self, user_id : int, name : str, mGame):
        self.Gamers[user_id] = RealGamer(user_id, name, mGame, self.base)
        self.List.append(self.Gamers[user_id])

    def start(self):
        self.id_to_map = list()
        self.lead = (self.lead + 1) % len(self.List)
        self.stage_id = 0
        for u in self.List:
            u.upd_media()
        self.isStart = 1

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
        if self.lead == -1:
            return
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
        text = "Статистика:\n"
        for u in self.List:
            if u.id != self.get_lead_id():
                text += '@' + u.name + " выбрал картинку " + str(u.ans + 1) + '\n'
        text += '\n'
        for u in self.List:
            for r in range(len(self.id_to_map)):
                if self.id_to_map[r] == u.id:
                    text += "у @" + u.name + " была карта " + str(r + 1) + '\n'
                    break
        text += "\nОчки:\n"
        for u in self.List:
            text += str(u.name) + ' : ' + str(u.score) + '\n'
        return text