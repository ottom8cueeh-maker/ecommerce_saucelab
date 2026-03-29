"""Shared data models and helpers used across all page objects."""
from asyncio.log import logger
from dataclasses import dataclass
from enum import Enum
from playwright.sync_api import Locator


class ProductName(Enum):
    """Canonical product names for all items available on SauceDemo."""
    BACKPACK = "Sauce Labs Backpack"
    BIKE_LIGHT = "Sauce Labs Bike Light"
    BOLT_T_SHIRT = "Sauce Labs Bolt T-Shirt"
    FLEECE_JACKET = "Sauce Labs Fleece Jacket"
    ONESIE = "Sauce Labs Onesie"
    ALL_THE_THINGS_T_SHIRT = "Test.allTheThings() T-Shirt (Red)"


@dataclass
class InventoryItem:
    """Represents a single product as it appears on inventory or cart pages."""
    name: str
    description: str
    price: float
    image_url: str = ""
    add_to_cart_button: Locator = None
    remove_from_cart_button: Locator = None


def extract_items(item_locator) -> list[InventoryItem]:
    """Extract name, description, and price from any page that uses the standard item layout (inventory or cart)."""
    count = item_locator.count()
    results = []

    for i in range(count):
        item = item_locator.nth(i)
        name = item.get_by_test_id("inventory-item-name").inner_text()
        price = float(item.get_by_test_id("inventory-item-price").inner_text().replace("$", ""))
        description = item.locator(".inventory_item_desc").inner_text()
        results.append(InventoryItem(name=name, price=price, description=description))

    return results

def add_to_cart(item: InventoryItem):
    """Click the 'Add to Cart' button for a given item."""
    if item.add_to_cart_button is not None:
        item.add_to_cart_button.click()
        logger.info("Add to Cart: %s", item.name)
    else:
        raise ValueError(f"Item '{item.name}' does not have an 'Add to Cart' button locator defined.")

def remove_from_cart(item: InventoryItem):
    """Click the 'Remove' button for a given item."""
    if item.remove_from_cart_button is not None:
        item.remove_from_cart_button.click()
        logger.info("Remove from Cart: %s", item.name)
    else:
        raise ValueError(f"Item '{item.name}' does not have a 'Remove from Cart' button locator defined.")

def get_item_prices(items: list[InventoryItem]) -> list[float]:
    """Helper function to extract just the prices from a list of InventoryItems."""
    return [item.price for item in items]
