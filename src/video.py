from src.channel import Channel


class ValidIdError(Exception):
    pass


class Video:

    def __init__(self, video_id='gaoc9MPZ4bw'):
        """Экземпляр инициализируется id видео"""
        try:
            self.video_id = video_id

            # получаем статистику видео по его id
            self.video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                id=self.video_id
                                                                ).execute()
            if len(self.video_response['items']) == 0:
                raise ValidIdError

        except ValidIdError:
            print("Видео с таким id не существует")
            self.video_title = None
            self.view_count = None
            self.like_count = None

        else:
            # ссылка на видео
            self.video_url = "https://www.youtube.com/watch?v=" + self.video_id

            # название видео
            self.video_title: str = self.video_response['items'][0]['snippet']['title']

            # количество просмотров
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']

            # количество лайков
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает название видео"""
        return f'{self.video_title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id="PLH-XmS0lSi_zdhYvcwUfv0N88LQRt6UZn"):
        """Инициализируется 'id видео' и 'id плейлиста' """
        super().__init__(video_id)
        self.playlist_id = playlist_id

        # получаем данные по видеороликам в плейлисте
        self.playlist_videos = Channel.youtube.playlistItems().list(playlistId=playlist_id,
                                                                    part='contentDetails',
                                                                    maxResults=50,
                                                                    ).execute()

        # получить все id видеороликов из плейлиста
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        # получаем статистику видео по его id
        self.video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                            id=','.join(self.video_ids)
                                                            ).execute()
