import os
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)

class Menu_Items:
    def __init__(self, page: Page):
        self.page = page
        self.menu_button = self.page.locator("#react-burger-menu-btn")
        self.logout = self.page.locator("#logout_sidebar_link")
        self.inventory = self.page.locator("#inventory_sidebar_link")
        self.menu_close = self.page.locator("#react-burger-cross-btn")
        self.reset_app_state = self.page.locator("#reset_sidebar_link")
        
    def open_menu(self):
        self.menu_button.click()    
        
    def click_logout(self):
        self.logout.click()
        
    def click_inventory(self):
        self.inventory.click()  
        
    def click_reset_app_state(self):
        self.reset_app_state.click()    
    
    def click_menu_close(self):
        self.menu_close.click()