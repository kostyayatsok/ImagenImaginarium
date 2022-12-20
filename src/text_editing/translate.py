import sentencepiece
from transformers import pipeline
model_checkpoint = "Helsinki-NLP/opus-mt-en-ru"
translator_for_Helsinki = pipeline("translation", model=model_checkpoint)
def translate_to_russia_with_Helsinki(text):
    return translator_for_Helsinki(text)[0]['translation_text']