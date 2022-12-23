import pandas as pd


base = pd.read_csv("Database.csv")

def get_photo(t : int):
    global base
    t += 1
    t %= base.shape[0]
    return base.iloc[t].img_path, t

def shuffle():
    global base
    base = base.sample(frac=1.)