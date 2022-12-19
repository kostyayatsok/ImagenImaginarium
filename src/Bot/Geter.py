from aiogram import Bot, types
from random import randint
from src.text_editing.bert_text_editor import edit_text_bert
from src.text_editing.edit_text_latent import edit_text_latent
from src.Bot.main import image_generation


def get_media(text):
    media = types.MediaGroup()
    emb_true = image_generation.text_embedding(text)
    image_true = image_generation.generate_image(emb_true)
    media.attach_photo(image_true)
    for i in range(2):
        new_text = edit_text_bert(text, 1)
        emb = image_generation.text_embedding(new_text)
        image = image_generation.generate_image(emb)
        media.attach_photo(image)
    for i in range(2):
        emb = image_generation.text_embedding(text)
        emb = edit_text_latent(emb, 7)
        image = image_generation.generate_image(emb)
        media.attach_photo(image)
    pos_who_must_replace = randint(0, 5)
    media[0], media[pos_who_must_replace] = media[pos_who_must_replace], media[0]
    return [media, pos_who_must_replace + 1, text]
