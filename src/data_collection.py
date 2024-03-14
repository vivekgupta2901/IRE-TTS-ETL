from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Set up the YouTube API client
DEVELOPER_KEY = 'YOUR_API_KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Define the search query and parameters
search_query = 'irish language'
max_results = 50

# Call the search.list method to retrieve video metadata
try:
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        maxResults=max_results
    ).execute()

    # Add video IDs to a list
    video_ids = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_ids.append(search_result['id']['videoId'])

    # Call the videos.list method to retrieve video details
    video_details = youtube.videos().list(
        id=','.join(video_ids),
        part='snippet,contentDetails'
    ).execute()

    # Create a directory to store the downloaded videos
    download_dir = 'downloaded_videos'
    os.makedirs(download_dir, exist_ok=True)

    # Download each video
    for video in video_details['items']:
        video_id = video['id']
        video_title = video['snippet']['title']
        video_filename = f"{video_id}.mp4"
        video_path = os.path.join(download_dir, video_filename)

        # Download the video
        print(f"Downloading video: {video_title}")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        os.system(f"youtube-dl -o '{video_path}' '{video_url}'")

except HttpError as e:
    print(f"An HTTP error occurred: {e}")