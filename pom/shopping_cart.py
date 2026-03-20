import logging
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from pom.menu import Menu_Items
from pom.items import InventoryItem, extract_items

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class ShoppingCart:
    def __init__(self, page: Page):
        """Initialize ShoppingCart with a Playwright Page and set up locators."""
        self.page = page
        self.menu = Menu_Items(page)
        self.checkout_button = self.page.locator("#checkout")        
        self.continue_shopping_button = self.page.locator("#continue-shopping")
        self.shopping_cart_icon = self.page.locator(".shopping_cart_link")
        self.shopping_cart_badge = self.page.locator(".shopping_cart_badge")
        self.items = self.page.locator(".cart_item")

    def get_items(self) -> list[InventoryItem]:
        """Return a list of InventoryItem objects currently in the cart, each with its remove button locator set."""
        results = extract_items(self.items)
        for i, item in enumerate(results):
            element = self.items.nth(i)
            item.remove_from_cart_button = element.get_by_role("button", name="Remove")
        return results
        
    def get_cart_items_count(self):
        """Return the number of items in the cart as shown by the cart badge, or 0 if the badge is not visible."""
        return int(self.shopping_cart_badge.inner_text()) if self.shopping_cart_badge.is_visible() else 0
    
    def click_shopping_cart_icon(self):
        """Wait for the page to load, assert the cart icon is visible and enabled, then click it."""
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.shopping_cart_icon).to_be_visible()
        expect(self.shopping_cart_icon).to_be_enabled()
        self.shopping_cart_icon.click()

    def click_checkout_button(self):
        """Click the checkout button to proceed to checkout."""
        self.checkout_button.click()

    def click_continue_shopping_button(self):
        """Click the continue shopping button to return to the inventory page."""
        self.continue_shopping_button.click()

    def get_remove_item_button_locator(self, item_name: str):
        """Return the locator for the remove button of the given item, identified by its display name."""
        # Convert item name to lowercase and replace spaces with hyphens to match the id format
        item_id = item_name.lower().replace(" ", "-")
        return self.page.locator(f"#remove-{item_id}")
    
    def remove_item_from_cart_on_cart_page(self, item_name: str):
        """Remove the specified item from the cart page and assert it is no longer visible."""
        remove_button = self.get_remove_item_button_locator(item_name)
        if remove_button.is_visible():
            remove_button.click()
            logger.info("Removed item '%s' from cart", item_name)
        else:
            logger.warning("Remove button for item '%s' not found in cart", item_name)
        # make sure the item is removed from cart by checking that the remove button is no longer visible
        assert not remove_button.is_visible(), f"Expected item '{item_name}' to be removed from cart, but it is still visible"
