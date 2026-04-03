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
        self.x_link = self.page.locator("a[href*='x.com']")
        self.facebook_link = self.page.locator("a[href*='facebook.com']")
        self.linkedin_link = self.page.locator("a[href*='linkedin.com']")
        self.twitter_link = self.page.locator("a[href*='twitter.com']")


    def get_image_count(self) -> int:
        """Return the total number of product images displayed on the page."""
        return self.items_image.count()

    def get_all_inventory_items(self) -> dict[str, InventoryItem]:
        """Return all inventory items on the page with their buttons and image URLs populated."""
        results = extract_items(self.items)

        for i, item in enumerate(results):
            element = self.items.nth(i)
            item.image_url = element.locator(".inventory_item_img img").get_attribute("src")
            item.add_to_cart_button = element.get_by_role("button", name="Add to cart")
            item.remove_from_cart_button = element.get_by_role("button", name="Remove")

        items_by_name = {item.name: item for item in results}
        return items_by_name


    def sort_items(self, sort_option: Literal["az", "za", "lohi", "hilo"]):
        """Sort the inventory items using the provided sort option."""
        self.product_sort_dropdown.select_option(sort_option)

    def click_item_name(self, item_name: str):
        """Click the item name to navigate to the inventory item details page."""
        self.page.get_by_text(item_name, exact=True).click()
        logger.info("Clicked on item name %s to navigate to inventory item details page", item_name)

class InventoryItemPage:
    """Encapsulates interactions with a single inventory item details page."""
    def __init__(self, page: Page):
        self.page = page
        self.back_to_products_button = self.page.locator("#back-to-products")
        self.add_to_cart_button = self.page.locator("#add-to-cart")
        self.remove_from_cart_button = self.page.locator("#remove")

    def add_to_cart(self) -> str:
        """Click the 'Add to Cart' button for the inventory item details page."""
        self.add_to_cart_button.click()
        logger.info("Inventory-item page: Added item to cart from inventory item details page")

    def remove_from_cart(self) -> str:
        """Click the 'Remove' button for the inventory item details page."""
        self.remove_from_cart_button.click()
        logger.info("Inventory-item page: Removed item from cart from inventory item details page")
