from src.Bot.main import dp
from aiogram.utils import executor
from src.image_generation.stable_diffusion import StableDiffusion

image_generation = StableDiffusion()

if __name__ == '__main__':
    executor.start_polling(dp)
