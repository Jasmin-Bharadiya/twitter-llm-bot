import os
from typing import Callable, List
import httpx
from openai import AsyncOpenAI

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_organization = os.getenv('OPENAI_ORG_ID')

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "OpenAI-Organization": openai_organization
}

client = AsyncOpenAI(
    api_key=openai_api_key,
    organization=openai_organization,
)

models = ["gpt-4-turbo-preview", "gpt-3.5-turbo", "dalle-3"]


async def generate_text_async(
    prompt,
    model=models[1],
    temperature=0.7,
    max_tokens=100,
    formatter: Callable[[str], List[str]] = None
):
    """
    Asynchronously generates text using the specified GPT model.

    Args:
        prompt (str): The input text prompt for the model.
        model (str): The model to use for generation ("gpt-3.5-turbo" or another GPT model).
        temperature (float): The temperature to use for the generation.
        max_tokens (int): The maximum number of tokens to generate.
    """
    chat_completion = await client.chat.completions.create(
        messages=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    raw_content = chat_completion.choices[0].message.content
    formatted_content = formatter(raw_content) if formatter else [raw_content]
    return formatted_content


async def generate_image_async(prompt, n=1, model=models[2]):
    """
    Asynchronously generates images using DALL·E 3 based on a text prompt.

    Args:
        prompt (str): The input text prompt for the image generation.
        n (int): Number of images to generate.
        model (str): The model to use for generation ("dalle-3").
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json={
                "model": model,
                "prompt": prompt,
                "n": n
            }
        )
        return response.json()