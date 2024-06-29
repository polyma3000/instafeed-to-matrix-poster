import instaloader
import asyncio
import os
from datetime import datetime, timedelta
from mautrix.client import Client
from mautrix.types import MessageType, TextMessageEventContent

# Function to scrape Instagram posts and reels
def scrape_instagram_content(username, scheduling_seconds):
    loader = instaloader.Instaloader()

    profile = instaloader.Profile.from_username(loader.context, username)

    scrape_starting_timestamp = datetime.now() - timedelta(seconds=scheduling_seconds)
    content = []
    for post in profile.get_posts():
        if post.date_utc > scrape_starting_timestamp:
            content.append({
                'link': f"https://www.instagram.com/p/{post.shortcode}/",
                'image': post.url,
                'caption': post.caption
            })

    # Scrape reels
    for post in profile.get_tagged_posts():
        if post.date_utc > scrape_starting_timestamp and post.typename == 'GraphVideo':
            content.append({
                'link': f"https://www.instagram.com/reel/{post.shortcode}/",
                'image': post.url,
                'caption': post.caption
            })

    return content

# Function to send messages to Matrix
async def send_matrix_messages(host, user_id, password, room_id, content):
    client = Client(host)

    try:
        await client.login(user_id, password)
    except Exception as e:
        print(f"Failed to log in: {e}")
        return

    for item in content:
        message_content = TextMessageEventContent(
            msgtype=MessageType.TEXT,
            body=f"Post: {item['link']}\nImage: {item['image']}\nCaption: {item['caption']}"
        )
        await client.send_message(room_id, message_content)

# Main function
async def main():
    instagram_username = os.getenv('INSTAGRAM_USERNAME')
    matrix_host = os.getenv('MATRIX_HOST')
    matrix_user_id = os.getenv('MATRIX_USER_ID')
    matrix_password = os.getenv('MATRIX_PASSWORD')
    matrix_room_id = os.getenv('MATRIX_ROOM_ID')
    sleep_time_seconds = os.getenv('SLEEP_TIME_SECONDS')

    content = scrape_instagram_content(instagram_username, sleep_time_seconds)
    await send_matrix_messages(matrix_host, matrix_user_id, matrix_password, matrix_room_id, content)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
