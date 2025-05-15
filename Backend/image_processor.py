import cv2
import numpy as np
from fastapi import UploadFile
from product_db import AmazonProductClient
import logging
from sklearn.cluster import KMeans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_image_search(file: UploadFile) -> list:
    db = AmazonProductClient()
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            logger.error("Failed to decode image")
            return [{"name": "Error", "description": "Invalid image file"}]

        # Improved color detection using k-means clustering
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixels = img_rgb.reshape(-1, 3)
        kmeans = KMeans(n_clusters=3, random_state=0)
        kmeans.fit(pixels)
        dominant_color = kmeans.cluster_centers_[0].astype(int)
        
        # Map to common color names (simplified)
        color_name = "blue" if dominant_color[2] > dominant_color[0] else "black"
        logger.info(f"Detected dominant color: {color_name}")

        # Search products by color
        products = await db.search_products(f"{color_name} t-shirt")
        if not products:
            return [{"name": "No Match", "description": "No products found for this image."}]
        return products

    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        return [{"name": "Error", "description": f"Failed to process image: {str(e)}"}]