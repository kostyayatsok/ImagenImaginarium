import torch

torch_device = "cuda" if torch.cuda.is_available() else "cpu"
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import AutoencoderKL, UNet2DConditionModel
from tqdm.auto import tqdm
from PIL import Image
from diffusers import LMSDiscreteScheduler


class StableDiffusion:
    def __init__(self):
        # 1. Load the autoencoder model which will be used to decode the latents into image space.
        self.vae = AutoencoderKL.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="vae")
        # 2. Load the tokenizer and text encoder to tokenize and encode the text.
        self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
        self.text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-large-patch14")
        # 3. The UNet model for generating the latents.
        self.unet = UNet2DConditionModel.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="unet")

        self.height = 512
        self.width = 512
        self.num_inference_steps = 100
        self.guidance_scale = 7.5
        self.generator = torch.manual_seed(32)
        self.batch_size = 1

        self.scheduler = LMSDiscreteScheduler.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="scheduler")
        self.scheduler.set_timesteps(self.num_inference_steps)
        self.vae = self.vae.to(torch_device)
        self.text_encoder = self.text_encoder.to(torch_device)
        self.unet = self.unet.to(torch_device)

    async def text_embedding(self, prompt):
        text_input = await self.tokenizer(prompt, padding="max_length", max_length=self.tokenizer.model_max_length,
                                    truncation=True, return_tensors="pt")
        with torch.no_grad():
            text_embeddings = await self.text_encoder(text_input.input_ids.to(torch_device))[0]

        max_length = text_input.input_ids.shape[-1]
        uncond_input = await self.tokenizer(
            [""] * self.batch_size, padding="max_length", max_length=max_length, return_tensors="pt"
        )
        with torch.no_grad():
            uncond_embeddings = await self.text_encoder(uncond_input.input_ids.to(torch_device))[0]
        text_embeddings = torch.cat([uncond_embeddings, text_embeddings])
        return text_embeddings

    async def generate_image(self, text_embeddings):
        # text_embeddings = self.text_embedding(prompt)
        latents = torch.randn(
            (self.batch_size, self.unet.in_channels, self.height // 8, self.width // 8),
            generator=self.generator,
        )
        latents = await latents.to(torch_device)
        latents = await latents * self.scheduler.init_noise_sigma

        for t in tqdm(self.scheduler.timesteps):
            # expand the latents if we are doing classifier-free guidance to avoid doing two forward passes.
            latent_model_input = torch.cat([latents] * 2)
            latent_model_input = await self.scheduler.scale_model_input(latent_model_input, t)
            # predict the noise residual
            with torch.no_grad():
                noise_pred = await self.unet(latent_model_input, t, encoder_hidden_states=text_embeddings).sample
            # perform guidance
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + self.guidance_scale * (noise_pred_text - noise_pred_uncond)
            # compute the previous noisy sample x_t -> x_t-1
            latents = await self.scheduler.step(noise_pred, t, latents).prev_sample

        # scale and decode the image latents with vae
        latents = 1 / 0.18215 * latents
        with torch.no_grad():
            image = await self.vae.decode(latents).sample
        image = (image / 2 + 0.5).clamp(0, 1)
        image = image.detach().cpu().permute(0, 2, 3, 1).numpy()
        images = (image * 255).round().astype("uint8")
        pil_images = [Image.fromarray(image) for image in images]
        return pil_images[0]

ImgGenerator = StableDiffusion()
