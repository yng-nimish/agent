class ProductDatabase:
    def __init__(self):
        self.products = [
            {"name": "Nike Dri-FIT T-shirt", "category": "t-shirt", "description": "moisture-wicking fabric", "color": "blue"},
            {"name": "Adidas Running T-shirt", "category": "t-shirt", "description": "lightweight and breathable", "color": "black"},
        ]

    def get_product_by_category(self, category: str, purpose: str = None) -> dict:
        for product in self.products:
            if product["category"] == category:
                return product
        return {"name": "Generic Product", "description": "suitable item"}

    def get_products_by_color(self, color: str) -> list:
        return [p for p in self.products if p["color"] == color]

    def get_all_products(self) -> str:
        return str(self.products)