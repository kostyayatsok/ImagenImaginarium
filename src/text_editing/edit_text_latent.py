import torch

torch_device = "cuda" if torch.cuda.is_available() else "cpu"


def edit_text_latent(text_embedding, noise_length):
    noise = torch.rand(text_embedding.shape)
    noise = noise.to(torch_device)
    l = torch.linalg.norm(noise)
    noise /= l
    noise *= noise_length
    new_text_embedding = text_embedding + noise
    return new_text_embedding
