import pandas as pd


base = pd.read_csv("Database.csv")

t = 0
def get_photo():
    global base, t
    t = (t + 1) % base.shape[0]
    return base.iloc[t].img_path

def shuffle():
    global base
    base = base.sample(frac=1.)