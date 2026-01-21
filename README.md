# 🏥 Medical Data Warehouse & Analytical Pipeline

**Medical Telegram Warehouse** is an end-to-end Data Engineering project that extracts, transforms, and analyzes medical business data from Ethiopian Telegram channels. It utilizes a modern ELT architecture to turn unstructured messages and images into actionable insights.

---

## 🚀 Key Features (Completed)

- **Telegram Scraping**: Automated extraction of messages, metadata, and images from channels (`CheMed`, `Lobelia`, `Tikvah`) using `Telethon`.
- **Data Lake & Warehousing**: Storage of raw JSON/Images and loading into a **PostgreSQL** Data Warehouse.
- **ELT Transformation**: robust data cleaning and Star Schema modeling using **dbt (Data Build Tool)**.
- **AI Object Detection**: Integration of **YOLOv8** to detect medical products (e.g., bottles, packaging) in scraped images.
- **Analytical API**: A REST API built with **FastAPI** to serve channel stats and AI insights.
- **Orchestration**: Fully automated pipeline management using **Dagster**.

---

## 📂 Project Structure

```bash
medical-telegram-warehouse/
├── api/                 # FastAPI application (main.py, schemas.py)
├── data/raw/            # Data Lake (JSONs and Images partitioned by date)
├── medical_warehouse/   # dbt project (Models: Staging -> Marts)
├── src/                 # Source scripts
│   ├── scraper.py       # Extract data from Telegram
│   ├── loader.py        # Load data to Postgres (Raw layer)
│   └── yolo_detect.py   # Run AI inference on images
├── orchestrator.py      # Dagster pipeline definition
├── docker-compose.yml   # Database service config
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```
## 🛠️ Tech Stack

- **Ingestion**: Python, Telethon
- **Database**: PostgreSQL
- **Transformation**: dbt Core
- **AI/ML**: YOLOv8 (Ultralytics)
- **API**: FastAPI, Uvicorn
- **Orchestration**: Dagster
- **Environment**: Docker, Dotenv
## ⚡ Setup Instructions
1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/eyuBirhanu/medical-telegram-warehouse.git
cd medical-telegram-warehouse
pip install -r requirements.txt
```
2. Environment Configuration
Create a .env file in the root directory:
```ini
# Telegram API Credentials (my.telegram.org)
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash

# Database Connection
# Format: postgresql://user:password@localhost:5432/dbname
DB_CONNECTION_STRING=postgresql://postgres:password@localhost:5432/medical_warehouse
```
3. Database Setup
Ensure you have a PostgreSQL database named medical_warehouse running (via Docker or Local).
```bash
# Optional: Run DB via Docker
docker-compose up -d
```
## 📊 How to Run the Pipeline
You have two options: run the automated orchestrator or run scripts manually.
Option A: Automated (Recommended)
Use Dagster to run Scraper -> Loader -> YOLO -> dbt in the correct order.
Start the Dagster UI:
```bash
dagster dev -f orchestrator.py
```
Open http://127.0.0.1:3000 in your browser.
Click "Launchpad" and then "Launch Run".
Option B: Manual Execution
Scrape Data:
```bash
python src/scraper.py
```
Load to DB:
```bash
python src/loader.py
```
Run Object Detection:
```bash
python src/yolo_detect.py
```
Transform Data:
```bash
cd medical_warehouse
dbt run
```
## 🌐 Running the API
Once the data is in the warehouse, you can serve it via the API.
Start the server:
```bash
uvicorn api.main:app --reload
```
Access the interactive documentation:
Go to: http://127.0.0.1:8000/docs
## 📄 License
This project is part of the Kifiya AI/Data Engineering training.