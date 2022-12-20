import random
from transformers import pipeline
import numpy as np


def normalize(p):
    s = sum(p)
    for i in range(len(p)):
        p[i] /= s
    return p


def edit_text_bert(text, num_masks):
    unmasker = pipeline('fill-mask', model='bert-base-uncased')
    words = text.split()
    for i in range(num_masks):
        position = random.randint(0, len(words) - 2)
        words[position] = '[MASK]'
        masked_text = ' '.join(words)
        variants = unmasker(masked_text)
        p = []
        w = []
        for d in variants:
            w.append(d['token_str'])
            p.append(d['score'])
        p = normalize(p)
        choice = np.random.choice(w, 1, p)
        words[position] = choice[0]
    new_text = ' '.join(words)
    return new_text

