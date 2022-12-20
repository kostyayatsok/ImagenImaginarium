from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import pandas as pd
base = pd.read_csv("Database.csv")

def get_photo():
    number_label = base.sample(1)["label"].values[0]
    img_paths = base[base["label"] == number_label]["img_path"].values
    return img_paths[0]