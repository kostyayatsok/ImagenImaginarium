from src.text_generation.gpt2 import generate_promt


def get_image(ImgGenerator, prompt=''):
    s = generate_promt(prompt)
    return ImgGenerator.generate_image(s)
