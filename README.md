# 🏥 Medical Telegram Warehouse

**Medical Telegram Warehouse** is a robust data engineering pipeline designed to collect, process, and analyze medical data sourced from Telegram channels. The project integrates scraping, data warehousing, and object detection to build a comprehensive medical data repository.

---

## 🚀 Key Features

- **Telegram Scraping**: Automated scraping of messages and images from specific medical Telegram channels (`lobelia4cosmetics`, `chemed`, `tikvahpharma`) using `Telethon`.
- **Data Ingestion**: Seamless loading of raw scraped data into a **PostgreSQL** database.
- **Data Transformation**: Implementation of **dbt (data build tool)** for cleaning, testing, and transforming raw data into a Star Schema (Facts and Dimensions).
- **Object Detection**: (Planned/In-progress) Integration of **YOLO** (`ultralytics`) for detecting objects in medical images.
- **API**: (In-progress) exposing data via **FastAPI**.
- **Orchestration**: Managed workflows using **Dagster**.

---

## 📂 Project Structure

```bash
medical-telegram-warehouse/
├── .github/workflows/   # CI/CD workflows
├── api/                 # FastAPI application
├── data/derived/        # Processed data
├── data/raw/            # Raw scraped data (images/json)
├── medical_warehouse/   # dbt project folder
│   ├── models/          # dbt models (staging, marts)
│   ├── analyses/        # dbt analyses
│   └── tests/           # dbt tests
├── notebooks/           # Jupyter notebooks for EDA and testing
├── scripts/             # Utility scripts
├── src/                 # Source code for scraper and loader
│   ├── scraper.py       # Telegram scraper script
│   └── loader.py        # Database loader script
├── tests/               # Unit and integration tests
├── .env                 # Environment variables
├── docker-compose.yml   # Docker services configuration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🛠️ Tech Stack

- **Language**: Python
- **Database**: PostgreSQL
- **Transformation**: dbt (Data Build Tool)
- **Scraping**: Telethon
- **Web Framework**: FastAPI
- **Computer Vision**: YOLOv8 (Ultralytics), OpenCV
- **Orchestration**: Dagster
- **Containerization**: Docker

---

## ⚡ Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Telegram API Credentials (`API_ID`, `API_HASH`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/eyuBirhanu/medical-telegram-warehouse.git
   cd medical-telegram-warehouse
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
   Create a `.env` file in the root directory and add your credentials:
   ```properties
   # Telegram API
   TG_API_ID=your_api_id
   TG_API_HASH=your_api_hash
   
   # Database
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=medical_warehouse
   
   # Database Connection String for Loader
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/medical_warehouse
   ```

---

## 📊 Usage

### 1. Scraping Data
Run the scraper to fetch latest messages and images from configured channels:
```bash
python src/scraper.py
```

### 2. Loading Data
Load the scraped JSON data into the PostgreSQL raw layer:
```bash
python src/loader.py
```

### 3. Running dbt Transformations
Navigate to the dbt project directory and run the models:
```bash
cd medical_warehouse
dbt run
```

To test the models:
```bash
dbt test
```

### 4. Running the API (Coming Soon)
```bash
uvicorn api.main:app --reload
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## 📄 License

This project is licensed under the MIT License.