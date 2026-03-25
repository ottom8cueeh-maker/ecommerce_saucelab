"""Page Object Model for the SauceDemo inventory (products) page."""
import logging
from typing import Literal
from dotenv import load_dotenv
from playwright.sync_api import Page
from pom.items import InventoryItem, extract_items

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class InventoryPage:
    """Encapsulates interactions with the inventory/products listing page."""

    def __init__(self, page: Page):
        """Initialise the page object and set up locators for inventory elements."""
        self.page = page
        self.items_filter_sorter = self.page.locator(".product_sort_container")
        self.items = self.page.locator(".inventory_item")
        self.items_image = self.page.locator(".inventory_item_img img")
        self.shopping_cart = self.page.locator(".shopping_cart_link")
        self.product_sort_dropdown = self.page.locator(".product_sort_container")


    def get_image_count(self) -> int:
        """Return the total number of product images displayed on the page."""
        return self.items_image.count()

    def get_all_inventory_items(self) -> list[InventoryItem]:
        """Return all inventory items on the page with their buttons and image URLs populated."""
        results = extract_items(self.items)

        for i, item in enumerate(results):
            element = self.items.nth(i)
            item.image_url = element.locator(".inventory_item_img img").get_attribute("src")
            item.add_to_cart_button = element.get_by_role("button", name="Add to cart")
            item.remove_from_cart_button = element.get_by_role("button", name="Remove")

        return results

    def sort_items(self, sort_option: Literal["az", "za", "lohi", "hilo"]):
        """Sort the inventory items using the provided sort option."""
        self.product_sort_dropdown.select_option(sort_option)

class InventoryItemPage:
    """Encapsulates interactions with a single inventory item details page."""
    def __init__(self, page: Page):
        self.page = page
        self.back_to_products_button = self.page.locator("#back-to-products")
        self.add_to_cart_button = self.page.locator("#add-to-cart")
        self.remove_from_cart_button = self.page.locator("#remove")
