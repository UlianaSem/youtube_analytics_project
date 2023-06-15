import datetime
import os

import googleapiclient.discovery
import isodate

import src.video


class PlayList:
    """Класс для ютуб-плейлиста"""
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.__playlist_id = playlist_id

        playlist = self.__get_info()

        self.title = playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + self.__playlist_id

    def __get_info(self):
        """Возвращает информацию о плейлисте."""
        youtube = self.get_service()
        playlist = youtube.playlists().list(id=self.__playlist_id, part='snippet,contentDetails').execute()

        return playlist

    def __get_video_ids(self):
        """Возвращает информацию по id видео в плейлисте"""
        youtube = self.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails',
                                                       maxResults=50, ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        return video_ids

    def __get_video_info(self):
        """Возвращает информацию по видеороликам в плейлисте"""
        youtube = self.get_service()
        video_ids = self.__get_video_ids()

        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)
                                               ).execute()

        return video_response

    @property
    def total_duration(self):
        """
        Возвращает общую продолжительность видео в плейлисте
        """
        total = datetime.timedelta()

        video_response = self.__get_video_info()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration

        return total

    def show_best_video(self):
        """
        Возвращает ссылки на самые популярные по количеству лайков видео в плейлисте
        """
        video_ids = self.__get_video_ids()

        videos = [src.video.Video(video_id) for video_id in video_ids]

        most_like = max([x.like_count for x in videos])
        best_videos = [x.url for x in videos if x.like_count == most_like]

        return ' '.join(best_videos)

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)
