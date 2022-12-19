from aiogram import Bot, types
import pandas as pd
from PIL import Image
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from random import randint
from src.image_generation.stable_diffusion import StableDiffusion
from src.text_editing.bert_text_editor import edit_text_bert
from src.text_editing.bert_text_editor import normalize
from src.text_editing.edit_text_latent import edit_text_latent
from src.Bot.main import image_generation
def get_media():
    media = []
    base = pd.read_csv('path')
    number_label = randint(0, 5)
    img_paths = base[base["label"] == number_label]["img_path"]
    texts = base[base["label"] == number_label]["text"]
    main_pictures = base[base["label"] == number_label]["main_picture"]
    img_paths_that_we_will_need = []
    str_true = ""
    for i in range(len(main_pictures)):
        if main_pictures[i]:
            str_true = texts[i]
            img_paths_that_we_will_need.append(img_paths)
            break
    ind = set()
    while len(ind) < 4:
        pos = randint(0, 5)
        if pos not in ind:
            ind.add(pos)
    ind = list(ind)
    for i in range(4):
        img_paths_that_we_will_need.append(img_paths[ind[i]])
    for i in range(5):
        media.append(Image.open(img_paths_that_we_will_need[i]))
    pos_who_must_replace = randint(0, 5)
    media[0], media[pos_who_must_replace] = media[pos_who_must_replace], media[0]
    return [media, pos_who_must_replace + 1, str_true]
