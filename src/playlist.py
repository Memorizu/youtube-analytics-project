import isodate
from src.video import Video
from src.channel import Channel
from datetime import timedelta


class PlayList:
    title = None
    url = None

    def __init__(self, playlist_id: int) -> None:
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.title = self.__title()

    @property
    def playlist(self):
        return Video.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                  part='contentDetails',
                                                  maxResults=50,
                                                  ).execute()

    @staticmethod
    def channel():
        return Channel.get_service()

    def play_list_data(self):
        return self.channel().playlistItems().list(playlistId=self.playlist_id,
                                                   part='contentDetails, id, snippet, status',
                                                   maxResults=50,
                                                   ).execute()

    def __title(self):
        yt_channel = self.channel()
        playlist_data = yt_channel.playlistItems().list(playlistId=self.playlist_id,
                                                        part='contentDetails, id, snippet, status',
                                                        maxResults=50,
                                                        ).execute()
        c_id = playlist_data["items"][0]["snippet"]["channelId"]
        playlist = yt_channel.playlists().list(channelId=c_id,
                                               part='contentDetails,snippet',
                                               maxResults=50,
                                               ).execute()

        for item in playlist['items']:
            if self.playlist_id == item['id']:
                return item['snippet']['title']

    @property
    def total_duration(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        video_response = Video.youtube.videos().list(part='contentDetails,statistics',
                                                     id=','.join(video_ids)
                                                     ).execute()

        total_duration = timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def get_video(self):
        all_video_id = [video['contentDetails']['videoId'] for video in self.play_list_data()['items']]
        channel = self.channel()
        return channel.videos().list(part='contentDetails,statistics',
                                     id=','.join(all_video_id)
                                     ).execute()

    def show_best_video(self):
        likes_count = 0
        cur_video_id = ''
        for item in self.get_video()['items']:
            if int(item['statistics']['likeCount']) > likes_count:
                likes_count = int(item['statistics']['likeCount'])
                cur_video_id = item['id']
        return f"https://youtu.be/{cur_video_id}"
