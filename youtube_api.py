import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = None
if API_KEY and API_KEY != "your_api_key_here":
    youtube = build('youtube', 'v3', developerKey=API_KEY)


# ---------------- EXTRACT INPUT ----------------
def extract_channel_input(user_input):
    user_input = user_input.strip()

    if "youtube.com/@" in user_input:
        return user_input.split("@")[-1]

    if "youtube.com/channel/" in user_input:
        return user_input.split("/")[-1]

    return user_input


# ---------------- GET CHANNEL DATA ----------------
def get_channel_data(user_input):

    channel_input = extract_channel_input(user_input)

    # Try as ID
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_input
    )
    response = request.execute()

    # If not found → search
    if 'items' not in response or len(response['items']) == 0:
        search_request = youtube.search().list(
            part="snippet",
            q=channel_input,
            type="channel",
            maxResults=1
        )
        search_response = search_request.execute()

        if len(search_response['items']) == 0:
            return None

        channel_id = search_response['items'][0]['snippet']['channelId']

        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

    if 'items' not in response or len(response['items']) == 0:
        return None

    data = response['items'][0]

    return {
        "title": data['snippet']['title'],
        "subs": int(data['statistics'].get('subscriberCount', 0)),
        "views": int(data['statistics'].get('viewCount', 0)),
        "videos": int(data['statistics'].get('videoCount', 0))
    }


# ---------------- GET VIDEOS ----------------
def get_videos(user_input):

    channel_input = extract_channel_input(user_input)

    # Search channel
    search_request = youtube.search().list(
        part="snippet",
        q=channel_input,
        type="channel",
        maxResults=1
    )
    search_response = search_request.execute()

    if len(search_response['items']) == 0:
        return []

    channel_id = search_response['items'][0]['snippet']['channelId']

    # Get videos
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=5,
        order="date"
    )
    response = request.execute()

    videos = []

    for item in response['items']:
        if item['id']['kind'] == "youtube#video":

            video_id = item['id']['videoId']

            stats_request = youtube.videos().list(
                part="statistics",
                id=video_id
            )
            stats_response = stats_request.execute()

            if len(stats_response['items']) == 0:
                continue

            stats = stats_response['items'][0]['statistics']

            videos.append({
                "title": item['snippet']['title'],
                "views": int(stats.get('viewCount', 0)),
                "likes": int(stats.get('likeCount', 0))
            })

    return videos
