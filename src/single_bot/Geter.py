from aiogram import types
import pandas as pd
from random import randint


    
def get_media(base):
    media_r = types.MediaGroup()

    main = base[base["main_picture"] == True].sample(1) 
    # other = base[base["main_picture"] != True].sample(4) 
    other = base[(base["label"] == main.iloc[0].label) & (~base.main_picture)]

    img_paths_that_we_will_need = [main.iloc[0].img_path]
    str_true = main.iloc[0].ru_text
    
    for path in other.img_path.values:
        img_paths_that_we_will_need.append(path)

    pos_who_must_replace = randint(0, len(img_paths_that_we_will_need)-1)
    img_paths_that_we_will_need[0], img_paths_that_we_will_need[pos_who_must_replace] = img_paths_that_we_will_need[pos_who_must_replace], img_paths_that_we_will_need[0]
    
    for i in range(len(img_paths_that_we_will_need)):
        media_r.attach_photo(types.InputFile(img_paths_that_we_will_need[i]))
    
    return media_r, pos_who_must_replace + 1, str_true
