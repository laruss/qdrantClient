import numpy
import torch
import clip
from PIL import Image
import requests
from io import BytesIO

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


"""
This module provides functions for getting image vectors.

WARN: This module requires the following packages:
    - torch: https://pytorch.org/
    - clip: https://github.com/openai/CLIP
    - PIL: https://pillow.readthedocs.io/
    - requests: https://docs.python-requests.org/
    - io: https://docs.python.org/3/library/io.html
    - BytesIO: https://docs.python.org/3/library/io.html#io.BytesIO
"""


def get_image_vector(image_url: str | None, image_path: str | None) -> numpy.ndarray:
    """
    Get image vector from URL or path
    Parameters:
        - image_url: str - URL of the image
        - image_path: str - path to the image
    Returns:
        - list[float] - image vector
    """
    if image_url is None and image_path is None:
        raise ValueError("Either image_url or image_path should be provided")
    if image_url:
        response = requests.get(image_url)
        bytes_ = BytesIO(response.content)
    else:
        bytes_ = open(image_path, "rb")
    image = Image.open(bytes_).convert("RGB")
    image = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()


def get_search_text_vector(search_text: str) -> numpy.ndarray:
    """
    Get search text vector
    Parameters:
        - search_text: str - search text
    Returns:
        - list[float] - search text vector
    """
    text = clip.tokenize([search_text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    return text_features.cpu().numpy()
