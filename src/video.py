import os

import googleapiclient.discovery


class Video:
    """Класс для ютуб-видео"""
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id

        video = self.__get_info()

        self.__video_title = video['items'][0]['snippet']['title']
        self.__url = "https://youtu.be/" + self.__video_id
        self.__view_count = int(video['items'][0]['statistics']['viewCount'])
        self.__like_count = int(video['items'][0]['statistics']['likeCount'])
        self.__comment_count = int(video['items'][0]['statistics']['commentCount'])

    def __str__(self):
        return self.__video_title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def video_title(self):
        return self.__video_title

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def comment_count(self):
        return self.__comment_count

    @property
    def url(self):
        return self.__url

    def __get_info(self):
        """Возвращает информацию о видео."""
        youtube = self.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.__video_id).execute()

        return video_response

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    """Класс для ютуб-видео с плейлистом"""
    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id видео и id плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)

        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
