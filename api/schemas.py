from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for Channel Activity
class ChannelStats(BaseModel):
    channel_name: str
    total_posts: int
    avg_views: float
    first_post_date: Optional[datetime]

# Schema for Message Search
class MessageResponse(BaseModel):
    message_id: int
    message_date: datetime
    message_text: Optional[str]
    views: int
    channel_name: str  # We will join this in the query

# Schema for Object Detection Stats
class DetectionStat(BaseModel):
    detected_class: str
    count: int

    class Config:
        from_attributes = True