import os
import json
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')

# Logging setup
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CHANNELS = [
    'https://t.me/lobelia4cosmetics',
    'https://t.me/chemed',
    'https://t.me/tikvahpharma'
]

async def scrape_channel(client, channel_url):
    channel_name = channel_url.split('/')[-1]
    logging.info(f"Starting scrape for {channel_name}")
    
    # Create directories
    today = datetime.now().strftime('%Y-%m-%d')
    json_dir = f"data/raw/telegram_messages/{today}"
    image_dir = f"data/raw/images/{channel_name}"
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    messages_data = []

    try:
        # Iterate over messages (limit to 100 for testing, remove limit for full scrape)
        async for message in client.iter_messages(channel_url, limit=100):
            msg_data = {
                "message_id": message.id,
                "channel_name": channel_name,
                "message_date": str(message.date),
                "message_text": message.text,
                "has_media": bool(message.media),
                "views": message.views,
                "forwards": message.forwards,
                "image_path": None
            }

            # Download Image if present
            if message.photo:
                path = await client.download_media(message.media, file=f"{image_dir}/{message.id}")
                msg_data['image_path'] = path

            messages_data.append(msg_data)

        # Save to JSON
        json_path = f"{json_dir}/{channel_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=4)
        
        logging.info(f"Successfully scraped {len(messages_data)} messages from {channel_name}")

    except Exception as e:
        logging.error(f"Error scraping {channel_name}: {e}")

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        for channel in CHANNELS:
            await scrape_channel(client, channel)

if __name__ == '__main__':
    asyncio.run(main())