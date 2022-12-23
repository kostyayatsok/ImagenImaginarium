import pandas as pd


def get_photo(base, t : int):
    t += 1
    t %= base.shape[0]
    return base.iloc[t].img_path, t

def shuffle(base):
    base = base.sample(frac=1.)