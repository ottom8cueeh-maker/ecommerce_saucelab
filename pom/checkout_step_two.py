import logging
from playwright.sync_api import Page
from pom.menu import Menu_Items
from pom.items import InventoryItem, extract_items

logger = logging.getLogger(__name__)

class CheckoutStepTwoPage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = Menu_Items(page)
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
        return extract_items(self.items)

    def get_payment_info(self) -> str:
        return self.payment_info_value.inner_text()
    
    def get_shipping_info(self) -> str:
        return self.shipping_info_value.inner_text()

    def get_summary_item_total_price(self) -> float:
        item_total_text = self.subtotal_value.inner_text()
        item_total_price = float(item_total_text.replace("Item total: $", ""))
        return item_total_price
    
    def get_summary_total_price(self) -> float:
        total_text = self.total_value.inner_text()
        total_price = float(total_text.replace("Total: $", ""))
        return total_price
    
    def get_summary_tax_price(self) -> float:
        tax_text = self.tax_value.inner_text()
        tax_price = float(tax_text.replace("Tax: $", ""))
        return tax_price
    
    def get_summary_total_price(self) -> float:
        total_text = self.total_value.inner_text()
        total_price = float(total_text.replace("Total: $", ""))
        return total_price

    def click_continue_button(self):
        self.continue_button.click()    

    def click_cancel_button(self):
        self.cancel_button.click()

    def click_finish_button(self):
        self.finish_button.click()