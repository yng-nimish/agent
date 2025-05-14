import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from product_db import ProductDatabase

load_dotenv()

class CommerceAgent:
    def __init__(self):
        self.db = ProductDatabase()
        self.name = "CommerceBot"
        # Configure OpenAI
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY"))

    async def handle_message(self, message: str) -> str:
        prompt = f"""
        You are CommerceBot, a shopping assistant for a commerce website. Your tasks:
        1. Handle general conversation (e.g., respond to "What's your name?" or "What can you do?").
        2. Provide product recommendations based on user input (e.g., "Recommend me a t-shirt for sports").
        3. Use the provided product database context to make accurate recommendations.
        Product Database: {self.db.get_all_products()}
        User Message: {message}
        Respond concisely and naturally, focusing on the user's intent.
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: Could not process request. {str(e)}"