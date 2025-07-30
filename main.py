# main.py
import ai_module
import data_handler
from browser_engine import BrowserEngine

# ⚠️ WARNING: This script uses exec() to run AI-generated code.
# This is powerful but carries risks. Only run in a secure, sandboxed environment.

def run_smart_agent(user_prompt: str, start_url: str, discovery_steps: int = 7):
    """
    Runs the agent with a discover-then-execute workflow.
    """
    engine = BrowserEngine(headless=False)
    engine.navigate(start_url)
    discovery_history = []
    
    ## -- PHASE 1: AI-GUIDED DISCOVERY --
    print("--- 🗺️ PHASE 1: AI-GUIDED DISCOVERY ---")
    for i in range(discovery_steps):
        print(f"\nDiscovery Step {i+1}/{discovery_steps}...")
        html = engine.get_clean_html()
        ai_code = ai_module.get_discovery_code(html, user_prompt, discovery_history)
        ai_code = ai_code.strip().removeprefix("```python").removesuffix("```").strip()

        print(f"🐍 AI suggests (cleaned): {ai_code}")
        
        try:
            # ADDED FOR DEBUGGING
            print("Executing discovery code...")
            exec(ai_code, {"page": engine.page})
            # ADDED FOR DEBUGGING
            print("Discovery code executed successfully.")
            
            discovery_history.append(ai_code)
            
            if "PATTERN_FOUND" in ai_code:
                print("✅ AI has identified the scraping pattern.")
                break
            engine.page.wait_for_timeout(2000)
        except Exception as e:
            print(f"🔥 Error during discovery: {e}")
            break
    else:
        print("⚠️ Discovery phase ended without finding a clear pattern.")

    ## -- PHASE 2: AI-POWERED GENERALIZATION --
    print("\n--- 🔨 PHASE 2: AI-POWERED GENERALIZATION ---")
    if not discovery_history:
        print("No successful discovery history. Cannot generate scraper. Exiting.")
        engine.close()
        return

    print("Asking AI to write the full scraper function...")
    scraper_function_code = ai_module.generate_scraper_function(discovery_history, user_prompt)
    scraper_function_code = scraper_function_code.strip().removeprefix("```python").removesuffix("```").strip()
    
    # --- UNCOMMENT THE LINE BELOW TO SEE THE FULL GENERATED SCRAPER ---
    print("\n--- GENERATED SCRAPER CODE ---\n")
    print(scraper_function_code)
    print("\n------------------------------\n")

    ## -- PHASE 3: AUTOMATED EXECUTION --
    print("\n--- 🚀 PHASE 3: AUTOMATED EXECUTION ---")
    try:
        local_scope = {}
        # ADDED FOR DEBUGGING
        print("Defining the generated scraper function...")
        exec(scraper_function_code, globals(), local_scope)
        scraper_func = local_scope.get('scrape_all_data')

        if scraper_func:
            # ADDED FOR DEBUGGING
            print("Executing the automated scraper function now...")
            scraped_data = scraper_func(engine.page)
            print(f"✅ Automated scrape complete! Found {len(scraped_data)} items.")
            
            data_handler.save_to_csv(scraped_data, user_prompt)
            print("\n📝 History update: 'Successfully scraped books.toscrape.com'")
        else:
            print("⚠️ Could not find the 'scrape_all_data' function in AI response.")
    except Exception as e:
        print(f"🔥 An error occurred during automated execution: {e}")

    engine.close()


if __name__ == "__main__":
    USER_PROMPT = "Scrape the title and price of every book on books.toscrape.com"
    START_URL = "https://books.toscrape.com/"
    
    run_smart_agent(USER_PROMPT, START_URL)