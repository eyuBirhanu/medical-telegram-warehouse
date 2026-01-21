from dagster import job, op
import subprocess
import os

# Op 1: Scrape Data
@op
def scrape_data():
    print("🚀 Starting Scraper...")
    result = subprocess.run(["python", "src/scraper.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraper failed: {result.stderr}")
    print("✅ Scraper finished.")
    return "Scraping Done"

# Op 2: Load Data to Postgres
@op
def load_data(start):
    print("🚀 Loading Data to DB...")
    result = subprocess.run(["python", "src/loader.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loader failed: {result.stderr}")
    print("✅ Data Loaded.")
    return "Loading Done"

# Op 3: Run YOLO Object Detection
@op
def run_yolo(start):
    print("🚀 Starting YOLO Detection...")
    result = subprocess.run(["python", "src/yolo_detect.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"YOLO failed: {result.stderr}")
    print("✅ YOLO finished.")
    return "YOLO Done"

# Op 4: Run dbt Transformations
@op
def run_dbt(start):
    print("🚀 Running dbt models...")
    # We need to be in the dbt folder to run dbt
    dbt_dir = os.path.join(os.getcwd(), "medical_warehouse")
    result = subprocess.run(["dbt", "run"], cwd=dbt_dir, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt failed: {result.stderr}")
    print(result.stdout)
    print("✅ dbt finished.")

# Define the Job (The Pipeline)
@job
def medical_pipeline_job():
    # 1. Run Scraper
    scraped = scrape_data()
    
    # 2. Run Loader (We pass 'scraped' into it so it waits for scraper to finish)
    loaded = load_data(scraped)
    
    # 3. Run YOLO (Waits for Loader)
    enriched = run_yolo(loaded)
    
    # 4. Run dbt (Waits for YOLO)
    run_dbt(enriched)


