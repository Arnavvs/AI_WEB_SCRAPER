# browser_engine.py
from playwright.sync_api import sync_playwright, Page, Playwright
from bs4 import BeautifulSoup # Import BeautifulSoup

class BrowserEngine:
    """
    A class to manage browser automation using Playwright.
    """
    def __init__(self, headless=True):
        """Initializes the browser engine."""
        self.playwright: Playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page: Page = self.browser.new_page()
        print("🤖 Browser engine started.")

    def navigate(self, url: str):
        """Navigates to a specific URL."""
        print(f"➡️ Navigating to {url}...")
        self.page.goto(url, wait_until="domcontentloaded")

    def get_clean_html(self) -> str:
        """
        Gets the page content and cleans it for the AI.
        Removes script, style, and other irrelevant tags.
        """
        html = self.page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # Remove irrelevant tags to reduce prompt size
        for tag in soup(['script', 'style', 'meta', 'link', 'header', 'footer']):
            tag.decompose()
        
        # Return the cleaned HTML of the body
        if soup.body:
            return str(soup.body)
        return str(soup) # Fallback

    # The rest of the file (execute_action, close) remains the same
    def execute_action(self, action: dict):
        action_type = action.get('action', '').upper()
        selector = action.get('selector')
        
        print(f"⚡ Executing action: {action_type} on selector '{selector}'")

        if action_type == "CLICK":
            if selector:
                self.page.click(selector, timeout=5000)
        elif action_type == "TYPE":
            text_to_type = action.get('text', '')
            if selector:
                self.page.fill(selector, text_to_type)
        else:
            print(f"⚠️ Unknown action type: {action_type}")
        
        self.page.wait_for_timeout(3000) 

    def close(self):
        """Closes the browser and stops the engine."""
        self.browser.close()
        self.playwright.stop()
        print("✅ Browser engine closed.")