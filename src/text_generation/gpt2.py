from transformers import pipeline
from random import randint


generator = pipeline('text-generation', model='Gustavosta/MagicPrompt-Stable-Diffusion')
generator_gpt = pipeline('text-generation', model='gpt2')

with open('nouns.txt', 'r') as f:
    nouns = f.readlines()
with open('verbs.txt', 'r') as f:
    verbs = f.readlines()
with open('adjectives.txt', 'r') as f:
    adjectives = f.readlines()
with open('phrases.txt', 'r') as f:
    phrases = f.readlines()


all_words = [nouns, verbs, adjectives, phrases]


def generate_promt():
    mode = randint(0, 3)
    words = all_words[mode]
    ind = randint(0, len(words)-1)
    return words[ind]


def generate_beu_promt(text=''):
    dct = generator(text, max_length=60, num_return_sequences=1)
    return dct[0]['generated_text']
