# data_handler.py
import pandas as pd
from datetime import datetime

def save_to_csv(data: list, user_prompt: str):
    """
    Saves a list of dictionaries to a CSV file.

    Args:
        data (list): The list of scraped data items.
        user_prompt (str): The original user prompt to generate a filename.
    """
    if not data:
        print("No data to save.")
        return

    # Create a simple filename from the prompt and timestamp
    safe_prompt = "".join(c for c in user_prompt if c.isalnum() or c in " _-").rstrip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scraped_results_{safe_prompt[:20]}_{timestamp}.csv"
    
    # Convert to a pandas DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"💾 Data successfully saved to {filename}")