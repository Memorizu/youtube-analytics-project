import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self.__update_attributes()
    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__get_build(), indent=2, ensure_ascii=False))

    def __update_attributes(self):
        """
        Записывает данные в атрибуты экземпляра класса.
        """
        data = self.__get_build()
        snippet = data['items'][0]['snippet']
        self.title = snippet['title']
        self.description = snippet['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = data['items'][0]['statistics']['subscriberCount']
        self.video_count = data['items'][0]['statistics']['videoCount']
        self.view_count = data['items'][0]['statistics']['viewCount']

    def __get_build(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_path) -> None:
        """Сохраняет значения атрибутов экземпляра Channel в JSON-файл"""
        data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

