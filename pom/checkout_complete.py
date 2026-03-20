import os
import logging
from playwright.sync_api import Page
from pom.menu import Menu_Items

logger = logging.getLogger(__name__)

class CheckoutCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = Menu_Items(page)
        self.complete_header = self.page.locator(".complete-header")
        self.complete_text = self.page.locator(".complete-text")
        self.back_home_button = self.page.locator("#back-to-products")
        self.checkout_status = self.page.locator('[data-test="title"]')


    def get_complete_header(self) -> str:
        return self.complete_header.inner_text()

    def get_complete_text(self) -> str:
        return self.complete_text.inner_text()

    def get_checkout_status(self) -> str:
        return self.checkout_status.inner_text()

    def click_back_home_button(self):
        self.back_home_button.click()