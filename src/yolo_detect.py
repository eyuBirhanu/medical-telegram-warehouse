import os
import logging
import pandas as pd
from ultralytics import YOLO
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Connect to DB
DB_STRING = os.getenv('DB_CONNECTION_STRING')
engine = create_engine(DB_STRING)

# Load Model (Nano version is fastest for CPU)
model = YOLO('yolov8n.pt')

def process_images():
    image_dir = "data/raw/images"
    detection_results = []

    logging.info("Starting Object Detection...")

    # Walk through channel folders
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(root, file)
                
                # Extract metadata from path
                # Path structure: data/raw/images/{channel_name}/{message_id}.jpg
                parts = image_path.split(os.sep)
                if len(parts) >= 2:
                    channel_name = parts[-2]
                    try:
                        message_id = int(file.split('.')[0])
                    except ValueError:
                        continue # Skip if filename isn't a number
                else:
                    continue

                try:
                    # Run YOLO Inference
                    results = model(image_path, verbose=False)
                    
                    # Process results
                    for r in results:
                        for box in r.boxes:
                            # Get class ID and confidence
                            cls_id = int(box.cls[0])
                            confidence = float(box.conf[0])
                            class_name = model.names[cls_id]
                            
                            # We only care about detections with > 50% confidence
                            if confidence > 0.5:
                                detection_results.append({
                                    "channel_name": channel_name,
                                    "message_id": message_id,
                                    "image_path": image_path,
                                    "detected_class": class_name,
                                    "confidence": confidence,
                                    "yolo_model": "yolov8n"
                                })
                except Exception as e:
                    logging.error(f"Error processing {image_path}: {e}")

    # Save to Database
    if detection_results:
        df = pd.DataFrame(detection_results)
        
        # Create schema if not exists
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.commit()
            
        logging.info(f"Saving {len(df)} detections to Database...")
        df.to_sql('image_detections', engine, schema='raw', if_exists='replace', index=False)
        logging.info("Done! Data saved to raw.image_detections")
    else:
        logging.warning("No detections found or no images found.")

if __name__ == "__main__":
    process_images()