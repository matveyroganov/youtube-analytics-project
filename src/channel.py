import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        # название канала
        self.title = "MoscowPython"

        # описание канала
        self.description = "Видеозаписи со встреч питонистов и джангистов в Москве и не только. :)/n" \
                           "Присоединяйтесь: https://www.facebook.com/groups/MoscowDjango! :)"

        # ссылка на канал
        self.url = "https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A"

        # количество подписчиков
        self.subscribers = 26000

        # количество видео
        self.video_count = 686

        # общее количество просмотров
        self.total_views = 2311490

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def dictionary_attributes(self):
        """
        Создаем словарь с атрибутами
        """
        attributes = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "total_views": self.total_views
        }
        return attributes

    def to_json(self, path):
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.dictionary_attributes(), file)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id
