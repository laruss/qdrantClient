import torch
from sentence_transformers import SentenceTransformer


class Encoder:
    encoder = SentenceTransformer(
        "all-MiniLM-L6-v2",
        device="cuda" if torch.cuda.is_available() else None,
    )


encoder = Encoder
