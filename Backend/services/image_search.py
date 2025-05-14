from transformers import CLIPProcessor, CLIPModel
import boto3
import faiss
import numpy as np
import os
from PIL import Image

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
index = faiss.IndexFlatL2(512)  # Dimension for CLIP

s3_client = boto3.client('s3')

# Sample product data (same as recommendation.py)
products = [
    {"id": "1", "name": "Sports T-Shirt", "price": 29.99},
    {"id": "2", "name": "Blue Sneakers", "price": 59.99},
]

# Initialize FAISS index for images (using text embeddings for simplicity)
embeddings = model.get_text_features(**processor(text=[p["name"] for p in products], return_tensors="pt")).detach().numpy()
index.add(embeddings)

def search_by_image(s3_path: str):
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    local_path = f"/tmp/{key.split('/')[-1]}"
    s3_client.download_file(bucket, key, local_path)
    
    image = Image.open(local_path)
    inputs = processor(images=image, return_tensors="pt")
    image_embedding = model.get_image_features(**inputs).detach().numpy()
    
    D, I = index.search(image_embedding, k=5)
    return [products[i] for i in I[0]]