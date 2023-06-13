import src.channel


class Video(src.channel.Channel):
    """Класс для ютуб-видео"""
    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id

        video = self.__get_info()

        self.__video_title = video['items'][0]['snippet']['title']
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

    def __get_info(self):
        """Возвращает информацию о видео."""
        youtube = self.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.__video_id).execute()

        return video_response


class PLVideo(Video):
    pass