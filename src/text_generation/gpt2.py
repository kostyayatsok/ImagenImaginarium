from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='gpt2')

def generate_promt(text=''):
    dct = generator(text, max_length=30, num_return_sequences=1)
    return dct[0]['generated_text']
