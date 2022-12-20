import pandas as pd
import os

from src.image_generation.stable_diffusion import StableDiffusion
from src.text_editing.bert_text_editor import edit_text_bert
from src.text_editing.edit_text_latent import edit_text_latent
from src.text_generation.gpt2 import generate_promt


LABEL = 1
PICTURE_NUMBER = 1
IMAGES_PATH = "Images"
DATABASE_PATH = "Database.csv"
TABLE = pd.read_csv(DATABASE_PATH)

image_generation = StableDiffusion()
os.makedirs(IMAGES_PATH, exist_ok=True)

def get_picture_name():
    global PICTURE_NUMBER
    number = str(PICTURE_NUMBER)
    PICTURE_NUMBER += 1
    while len(number) < 6:
        number = '0' + number
    return 'IMG' + number + ".png"


def add_table_row(img_path, label, text, main_picture):
    global TABLE
    TABLE = TABLE.append(pd.DataFrame({
        "img_path": [img_path],
        "label": [label],
        "text": [text],
        "main_picture": [main_picture]
    }), ignore_index=True)


def save():
    TABLE.to_csv(DATABASE_PATH, index=False)


def add_media(text=""):
    global LABEL
    global IMAGES_PATH
    text = generate_promt(text)
    emb_true = image_generation.text_embedding(text)
    image_true = image_generation.generate_image(emb_true)
    picture_name = get_picture_name()
    img_path = IMAGES_PATH + '\\' + picture_name
    add_table_row(img_path, LABEL, text, "True")
    image_true.save(img_path)
    for _ in range(2):
        new_text = edit_text_bert(text, 1)
        emb = image_generation.text_embedding(new_text)
        image = image_generation.generate_image(emb)
        picture_name = get_picture_name()
        img_path = IMAGES_PATH + '\\' + picture_name
        add_table_row(img_path, LABEL, new_text, "False")
        image.save(img_path)
    for _ in range(2):
        emb = image_generation.text_embedding(text)
        emb = edit_text_latent(emb, 7)
        image = image_generation.generate_image(emb)
        picture_name = get_picture_name()
        img_path = IMAGES_PATH + '\\' + picture_name
        add_table_row(img_path, LABEL, "None", "False")
        image.save(img_path)
    if LABEL % 10 == 0:
        save()
    LABEL += 1
    return


if __name__ == "__main__":
    add_media()
