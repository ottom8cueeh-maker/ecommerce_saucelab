import logging
from dotenv import load_dotenv
from playwright.sync_api import Page
from pom.items import InventoryItem, extract_items


# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items_filter_sorter = self.page.locator(".product_sort_container")
        self.items = self.page.locator(".inventory_item")
        self.items_image = self.page.locator(".inventory_item_img img")
        self.shopping_cart = self.page.locator(".shopping_cart_link")

    def get_image_count(self) -> int:
        return self.items_image.count()
    
    def get_all_inventory_items(self) -> list[InventoryItem]:
        results = extract_items(self.items)

        for i, item in enumerate(results):
            element = self.items.nth(i)
            item.image_url = element.locator(".inventory_item_img img").get_attribute("src")
            item.add_to_cart_button = element.get_by_role("button", name="Add to cart")
            item.remove_from_cart_button = element.get_by_role("button", name="Remove")

        return results
