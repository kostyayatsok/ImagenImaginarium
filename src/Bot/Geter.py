from aiogram import Bot, types
from random import randint
from src.text_editing.bert_text_editor import edit_text_bert
from src.text_editing.edit_text_latent import edit_text_latent
from src.image_generation.stable_diffusion import StableDiffusion

image_generation = StableDiffusion()


def get_media(text):
    media = list()
    media_r = types.MediaGroup()
    emb_true = image_generation.text_embedding(text)
    print("embedding getted")
    image_true = image_generation.generate_image(emb_true)
    print("first picture generated")
    media.append(image_true)
    for i in range(2):
        new_text = edit_text_bert(text, 1)
        emb = image_generation.text_embedding(new_text)
        image = image_generation.generate_image(emb)
        media.append(image)
    for i in range(2):
        emb = image_generation.text_embedding(text)
        emb = edit_text_latent(emb, 7)
        image = image_generation.generate_image(emb)
        media.append(image)
    pos_who_must_replace = randint(0, 5)
    media[0], media[pos_who_must_replace] = media[pos_who_must_replace], media[0]
    for i in range(0, 5):
        media_r.attach_photo(media[i])
    print("replaced")
    return [media, pos_who_must_replace + 1, text]
