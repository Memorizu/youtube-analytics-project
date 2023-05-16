import os
from dotenv import load_dotenv, find_dotenv
from googleapiclient.discovery import build


# Как правильно импортировать и применять библиотеку dotenv?
load_dotenv(find_dotenv())


class Video:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.title = self.video_title()
        self.url_video = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = self.view_count()
        self.likes_count = self.likes_count()

    def __str__(self) -> str:
        return self.title

    def _video_stat(self):
        return self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=self.video_id
                                          ).execute()

    def video_title(self):
        stat = self._video_stat()
        return stat['items'][0]['snippet']['title']

    def view_count(self):
        stat = self._video_stat()
        return stat['items'][0]['statistics']['viewCount']

    def likes_count(self):
        stat = self._video_stat()
        return stat['items'][0]['statistics']['likeCount']
