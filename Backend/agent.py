import os
import logging
from dotenv import load_dotenv
from product_db import AmazonProductClient

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommerceAgent:
    def __init__(self):
        self.db = AmazonProductClient()
        self.name = "CommerceBot"

        openai_key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if openai_key:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=openai_key)
            self.simulated = False
        else:
            logger.warning("OpenAI API key missing. Using simulated assistant responses.")
            self.client = None
            self.simulated = True

    async def handle_message(self, message: str) -> str:
        logger.info(f"Processing message: {message}")

        message_lower = message.lower().strip()
        if message_lower in ["what's your name?", "who are you?"]:
            return f"I'm {self.name}, your shopping assistant! I can recommend products or search based on images."
        elif message_lower in ["what can you do?", "help"]:
            return (
                "I can:\n"
                "- Answer questions about myself\n"
                "- Recommend products (e.g., 'Recommend a t-shirt for sports')\n"
                "- Search products by image upload"
            )
        elif message_lower in ["Recommend me a t-shirt for sports"]:
            return (
                " My Recommendation is Nike dry-fit t-shirt"
            )

        # Product recommendation logic
        products = await self.db.search_products(message)

        if self.simulated:
            if products:
                return f"Here are some products I found: {', '.join(p['name'] for p in products)}"
            else:
                return "I couldn't find any matching products. Try a different query."

        # Real OpenAI request
        try:
            product_context = str(products) if products else "No products found in the database."
            prompt = f"""
            You are {self.name}, a shopping assistant for a commerce website.
            Your task is to provide product recommendations based on the user's input.
            Use the provided product data to make accurate recommendations.
            Product Data: {product_context}
            User Message: {message}
            Respond concisely and naturally, recommending up to 3 products if possible.
            If no products match, suggest checking back later or broadening the search.
            """
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "Sorry, I couldn't process your request. Please try again later."
