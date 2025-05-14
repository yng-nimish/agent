import cv2
import numpy as np
from fastapi import UploadFile
from product_db import ProductDatabase

async def process_image_search(file: UploadFile):
    db = ProductDatabase()
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Simple color-based matching (OpenAI vision not used due to API limitations)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    dominant_color = "blue" if hist[4, 4, 4] > hist[0, 0, 0] else "black"
    products = db.get_products_by_color(dominant_color)
    return products if products else [{"name": "No Match", "description": "No products found for this image."}]