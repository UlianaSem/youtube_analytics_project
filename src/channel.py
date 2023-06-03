import json
import os

import googleapiclient.discovery


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = self.__get_info()

        self.__title = channel['items'][0]['snippet']['title']
        self.__channel_description = channel['items'][0]['snippet']['description']
        self.__url = "https://www.youtube.com/channel/" + channel_id
        self.__subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.__video_count = channel['items'][0]['statistics']['videoCount']
        self.__view_count = channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def channel_description(self):
        return self.__channel_description

    @property
    def url(self):
        return self.__url

    @property
    def subscriber_count(self):
        return self.__subscriber_count

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def __get_info(self):
        """Возвращает информацию о канале."""
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        return channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.__get_info()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name: str):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        path = '../src/' + file_name.strip()

        with open(path, 'w') as file:
            file.write(f'id: {self.__channel_id}\n')
            file.write(f'title: {self.__title}\n')
            file.write(f'description: {self.__channel_description}\n')
            file.write(f'url: {self.__url}\n')
            file.write(f'subscriber_count: {self.__subscriber_count}\n')
            file.write(f'video_count: {self.__video_count}\n')
            file.write(f'view_count: {self.__view_count}\n')
