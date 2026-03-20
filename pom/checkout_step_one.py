import os
import logging
from playwright.sync_api import Page
from pom.menu import Menu_Items

logger = logging.getLogger(__name__)

class CheckoutStepOnePage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = Menu_Items(page)
        self.first_name_input = self.page.locator("#first-name")
        self.last_name_input = self.page.locator("#last-name")
        self.postal_code_input = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")
        self.cancel_button = self.page.locator("#cancel")
    
    def enter_first_name(self, first_name: str):
        self.first_name_input.fill(first_name)
    
    def enter_last_name(self, last_name: str):
        self.last_name_input.fill(last_name)

    def enter_postal_code(self, postal_code: str):
        self.postal_code_input.fill(postal_code)
    
    def click_continue_button(self):
        self.continue_button.click()
    
    def click_cancel_button(self):
        self.cancel_button.click()
        