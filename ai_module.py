# ai_module.py
import os
import google.generativeai as genai
from dotenv import load_dotenv # Import the library

load_dotenv()

try:
    # This line now works because load_dotenv() has loaded the key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError: # Changed the error type to be more specific
    print("🚨 GOOGLE_API_KEY not found. Make sure it's in your .env file.")
    exit()

model = genai.GenerativeModel('gemini-1.5-flash')

def get_discovery_code(html_content: str, user_prompt: str, history: list) -> str:
    """
    [Phase 1] Generates a single Playwright command to discover the site structure.
    """
    system_prompt = f"""
    You are a web scraping agent in "discovery mode". Your goal is to understand the structure of a site to fulfill the user's request: "{user_prompt}".
    Your task is to write a single snippet of Python code for the *next step*. The code will use a Playwright object named `page`.

    - First, understand the page (search, lists, etc.).
    - Then, identify the selectors for the required data (titles, prices, etc.).
    - Finally, identify the selector for the "next page" button.
    - Once you have successfully scraped the first page and located the 'next' button, your command should be: `print("PATTERN_FOUND")`
    - Your response MUST be only the Python code.
    - if no history obviously start new, everything depends on your first command.
    - If you have already executed commands, use the following history to inform your next step:

    History of commands executed so far: {history}
    """
    response = model.generate_content([system_prompt, "Current HTML:", html_content])
    return response.text.strip()


def generate_scraper_function(history: list, user_prompt: str) -> str:
    """
    [Phase 2] Analyzes the discovery history to write a complete, looping scraper function.
    """
    system_prompt = f"""
    You are a code generation assistant. Based on the successful Playwright command history, create a single Python function named `scrape_all_data`.
    This function should take a Playwright `page` object as its only argument.

    The function must:
    1.  Loop through all pages of the website using the "next" button pattern found in the history.
    2.  On each page, scrape the data points (like titles, prices, etc.) identified in the history.
    3.  Store the scraped data in a list of dictionaries.
    4.  Handle potential errors gracefully with try/except blocks.
    5.  Return the list of all scraped data.
    6.  Your response must be ONLY the Python function code, nothing else.

    User's high-level goal: "{user_prompt}"
    Successful discovery command history:
    {history}
    """
    response = model.generate_content(system_prompt)
    return response.text.strip()