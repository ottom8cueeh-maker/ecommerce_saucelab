"""Page Object Model for the SauceDemo checkout step two (order summary) page."""
import logging
from playwright.sync_api import Page
from pom.menu import MenuItems
from pom.items import InventoryItem, extract_items

logger = logging.getLogger(__name__)

class CheckoutStepTwoPage:
    """Encapsulates interactions with the checkout step two (order review) page."""

    def __init__(self, page: Page):
        """Initialise the page object and set up locators for all summary elements."""
        self.page = page
        self.menu = MenuItems(page)
        self.payment_info_value = self.page.locator("[data-test='payment-info-value']")
        self.shipping_info_value = self.page.locator("[data-test='shipping-info-value']")
        self.subtotal_value = self.page.locator(".summary_subtotal_label")
        self.tax_value = self.page.locator(".summary_tax_label")
        self.total_value = self.page.locator(".summary_total_label")
        self.continue_button = self.page.locator("#continue")
        self.cancel_button = self.page.locator("#cancel")
        self.finish_button = self.page.locator("#finish")
        self.items = self.page.locator(".cart_item")

    def get_items(self) -> list[InventoryItem]:
        """Return the list of items shown in the order summary."""
        return extract_items(self.items)

    def get_payment_info(self) -> str:
        """Return the payment information label text."""
        return self.payment_info_value.inner_text()

    def get_shipping_info(self) -> str:
        """Return the shipping information label text."""
        return self.shipping_info_value.inner_text()

    def get_summary_item_total_price(self) -> float:
        """Return the item subtotal (before tax) as a float."""
        item_total_text = self.subtotal_value.inner_text()
        item_total_price = float(item_total_text.replace("Item total: $", ""))
        return item_total_price

    def get_summary_total_price(self) -> float:
        """Return the order total (items + tax) as a float."""
        total_text = self.total_value.inner_text()
        total_price = float(total_text.replace("Total: $", ""))
        return total_price

    def get_summary_tax_price(self) -> float:
        """Return the tax amount as a float."""
        tax_text = self.tax_value.inner_text()
        tax_price = float(tax_text.replace("Tax: $", ""))
        return tax_price

    def click_continue_button(self):
        """Click the Continue button (unused on this page but available for completeness)."""
        self.continue_button.click()

    def click_step2_cancel_button(self):
        """Click the Cancel button to return to the cart."""
        self.cancel_button.click()
        logger.info("Clicking cancel button...")

    def click_finish_button(self):
        """Click the Finish button to complete the purchase."""
        self.finish_button.click()
        logger.info("Clicking finish button...")
