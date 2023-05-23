import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

os.environ['YT_API_KEY'] = 'AIzaSyDmvodVAPDoWVMQhSDRvRWZtDEgC2Joijw'


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        self.api_key: str = os.getenv('YT_API_KEY')

        # создать специальный объект для работы с API
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
