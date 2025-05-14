from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # Dimension for all-MiniLM-L6-v2

# Sample product data
products = [
    {"id": "1", "name": "Sports T-Shirt", "price": 29.99},
    {"id": "2", "name": "Blue Sneakers", "price": 59.99},
]

# Initialize FAISS index
embeddings = model.encode([p["name"] for p in products])
index.add(np.array(embeddings))

def get_recommendations(query: str):
    query_embedding = model.encode([query])[0]
    D, I = index.search(np.array([query_embedding]), k=5)
    return [products[i] for i in I[0]]