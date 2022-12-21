import pandas as pd
import os
import argparse

from src.image_generation.stable_diffusion import StableDiffusion
from src.text_editing.bert_text_editor import edit_text_bert
from src.text_editing.edit_text_latent import edit_text_latent
from src.text_generation.gpt2 import generate_promt

LABEL = 1
IMAGES_PATH = "Images"
DATABASE_PATH = "Database.csv"
MAX_DATABASE_SIZE = 1000

if os.path.exists(DATABASE_PATH):
    TABLE = pd.read_csv(DATABASE_PATH)
else:
    TABLE = pd.DataFrame()

image_generation = StableDiffusion()
os.makedirs(IMAGES_PATH, exist_ok=True)


def get_picture_name(pic):
    return f"{IMAGES_PATH}/{LABEL:05d}_{pic:02d}.png"


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


def delete(label):
    global TABLE
    TABLE = TABLE[TABLE.label != label]


def add_media(num_masks, noise_length, n_bert_images, n_noise_images):
    global LABEL

    delete(LABEL)

    is_nsfw = True
    while is_nsfw:
        text = generate_promt()
        emb_true = image_generation.text_embedding(text)
        image_true, is_nsfw = image_generation.generate_image(emb_true)
    img_path = get_picture_name(0)
    add_table_row(img_path, LABEL, text, "True")
    image_true.save(img_path)

    for j in range(n_bert_images):
        is_nsfw = True
        while is_nsfw:
            new_text = edit_text_bert(text, num_masks)
            emb = image_generation.text_embedding(new_text)
            image, is_nsfw = image_generation.generate_image(emb)

        img_path = get_picture_name(j + 1)
        add_table_row(img_path, LABEL, new_text, False)
        image.save(img_path)

    for j in range(n_noise_images):
        is_nsfw = True
        while is_nsfw:
            emb = edit_text_latent(emb_true, noise_length)
            image, is_nsfw = image_generation.generate_image(emb)

        img_path = get_picture_name(j + 1 + n_bert_images)
        add_table_row(img_path, LABEL, None, False)
        image.save(img_path)

    LABEL = (LABEL + 1) % MAX_DATABASE_SIZE


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--num_masks', type=int, default=5,
                        help='how many tokens masked')
    parser.add_argument('--noise_length', type=int, default=5,
                        help='noise_length')
    parser.add_argument('--n_bert_images', type=int, default=2,
                        help='how many images generate with masking strategy')
    parser.add_argument('--n_noise_images', type=int, default=2,
                        help='how many images generate with noise strategy')
    parser.add_argument('--n_iterations', type=int, default=1000,
                        help='how many sample to generate to do. -1 for endless generation.')
    parser.add_argument('--images_path', type=str, default='Images',
                        help='where images are stored')
    parser.add_argument('--database_path', type=str, default='Database.csv',
                        help='where database is stored')
    parser.add_argument('--max_database_size', type=int, default=1000,
                        help='max_number_of_rows_in_database')

    args = parser.parse_args()

    IMAGES_PATH = args.images_path
    DATABASE_PATH = args.database_path
    MAX_DATABASE_SIZE = args.max_database_size

    if TABLE.shape[0] != 0:
        d = TABLE.iloc[-1]
        LABEL = (d["label"] + 1) % MAX_DATABASE_SIZE

    iterations_done = 0

    while args.n_iterations == -1:
        try:
            add_media(args.num_masks, args.noise_length, args.n_bert_images, args.n_noise_images)
            iterations_done += 1
            if iterations_done % 5 == 0:
                save()
        except:
            pass

    for i in range(args.n_iterations):
        try:
            add_media(args.num_masks, args.noise_length, args.n_bert_images, args.n_noise_images)
            iterations_done += 1
            if iterations_done % 5 == 0:
                save()
        except:
            pass

    save()
