from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import database, schemas

app = FastAPI(title="Medical Data Warehouse API", description="API for Ethiopian Medical Telegram Data")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the Medical Data API"}

# Endpoint 1: Get Channel Statistics
@app.get("/channels", response_model=list[schemas.ChannelStats])
def get_channels(db: Session = Depends(database.get_db)):
    """Returns a list of channels and their performance stats."""
    query = text("SELECT channel_name, total_posts, avg_views, first_post_date FROM marts.dim_channels")
    result = db.execute(query).fetchall()
    
    # Convert rows to dictionaries
    return [
        {
            "channel_name": row.channel_name,
            "total_posts": row.total_posts,
            "avg_views": row.avg_views,
            "first_post_date": row.first_post_date
        } 
        for row in result
    ]

# Endpoint 2: Search Messages
@app.get("/messages/search", response_model=list[schemas.MessageResponse])
def search_messages(keyword: str, limit: int = 10, db: Session = Depends(database.get_db)):
    """Search for messages containing a specific keyword."""
    # We join fct_messages with dim_channels to get the channel name
    query = text("""
        SELECT m.message_id, m.message_date, m.message_text, m.views, c.channel_name
        FROM marts.fct_messages m
        JOIN marts.dim_channels c ON m.channel_key = c.channel_key
        WHERE m.message_text ILIKE :keyword
        ORDER BY m.message_date DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"keyword": f"%{keyword}%", "limit": limit}).fetchall()
    
    return [
        {
            "message_id": row.message_id,
            "message_date": row.message_date,
            "message_text": row.message_text,
            "views": row.views,
            "channel_name": row.channel_name
        }
        for row in result
    ]

# Endpoint 3: Visual Content Stats (YOLO)
@app.get("/images/stats", response_model=list[schemas.DetectionStat])
def get_image_stats(db: Session = Depends(database.get_db)):
    """Returns the top detected objects in images."""
    query = text("""
        SELECT detected_class, COUNT(*) as count
        FROM marts.fct_image_detections
        GROUP BY detected_class
        ORDER BY count DESC
    """)
    result = db.execute(query).fetchall()
    
    return [{"detected_class": row.detected_class, "count": row.count} for row in result]