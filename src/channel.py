import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = 'AIzaSyAtqCp_NG6X4zhiED7BmpEtYAW9F_4VBnE'

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__get_build(), indent=2, ensure_ascii=False))

    def __get_build(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel
