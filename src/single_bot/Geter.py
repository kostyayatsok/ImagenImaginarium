from aiogram import types
import pandas as pd
from random import randint


base = pd.read_csv("Database.csv")
    
def get_media():
    media_r = types.MediaGroup()

    number_label = base.sample(1)["label"].values[0]
    img_paths = base[base["label"] == number_label]["img_path"].values
    texts = base[base["label"] == number_label]["text"].values
    main_pictures = base[base["label"] == number_label]["main_picture"].values
    
    cnt_pictures = min(10, len(texts))
    
    img_paths_that_we_will_need = []
    str_true = ""
    for i in range(len(main_pictures)):
        if main_pictures[i] == True:
            str_true = texts[i]
            img_paths_that_we_will_need.append(img_paths[i])
            break

    ind = set()
    while len(ind) < cnt_pictures - 1:
        pos = randint(0, cnt_pictures - 1)
        if pos not in ind and main_pictures[pos] == 0:
            ind.add(pos)
    
    ind = list(ind)
    for i in range(len(ind)):
        img_paths_that_we_will_need.append(img_paths[ind[i]])
    
    for i in range(len(img_paths_that_we_will_need)):
        img_paths_that_we_will_need[i] = img_paths_that_we_will_need[i]
    
    pos_who_must_replace = randint(0, len(img_paths_that_we_will_need)-1)
    img_paths_that_we_will_need[0], img_paths_that_we_will_need[pos_who_must_replace] = img_paths_that_we_will_need[pos_who_must_replace], img_paths_that_we_will_need[0]
    
    for i in range(len(img_paths_that_we_will_need)):
        media_r.attach_photo(types.InputFile(img_paths_that_we_will_need[i]))
    
    return media_r, pos_who_must_replace + 1, str_true
