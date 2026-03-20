"""Page Object Model for the inventory items on the SauceDemo inventory and cart pages.
This module defines the InventoryItem dataclass and a helper function to extract item details from any page that uses the standard item layout."""
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
