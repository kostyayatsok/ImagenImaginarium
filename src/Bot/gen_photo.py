import pandas as pd


base = pd.read_csv("Database.csv")

t = 0
def get_photo():
    return base.sample(1).iloc[0].img_path
