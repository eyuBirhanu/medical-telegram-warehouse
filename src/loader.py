import os
import json
import pandas as pd
from sqlalchemy import create_engine, text  # Import text here
from dotenv import load_dotenv

load_dotenv()
DB_STRING = os.getenv('DB_CONNECTION_STRING')

def load_data():
    # check if connection string is present
    if not DB_STRING:
        raise ValueError("DB_CONNECTION_STRING not found in .env file")

    engine = create_engine(DB_STRING)
    raw_dir = "data/raw/telegram_messages"
    
    all_data = []
    
    # Walk through the directory to find all JSON files
    for root, dirs, files in os.walk(raw_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_data.extend(data)
                        else:
                            all_data.append(data)
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    if not all_data:
        print("No data found to load. Make sure you ran the scraper first!")
        return

    df = pd.DataFrame(all_data)
    
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit() 

    print(f"Loading {len(df)} rows to database...")
    df.to_sql('telegram_messages', engine, schema='raw', if_exists='replace', index=False)
    print("Success! Data loaded into raw.telegram_messages")

if __name__ == "__main__":
    load_data()