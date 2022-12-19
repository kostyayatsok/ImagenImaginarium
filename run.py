from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from src.Bot.config import TOKEN
from aiogram.utils import executor
from src.image_generation.stable_diffusion import StableDiffusion

image_generation = StableDiffusion()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp)
    print("polling")
