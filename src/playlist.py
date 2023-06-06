from src.channel import Channel
# Импорт классов для работы с данными
import datetime
import isodate


class Playlist:
    def __init__(self, playlist_id):
        """Инициализируется _id_ плейлиста"""

        self.playlist_id = playlist_id

        # название плейлиста
        self.title = "Moscow Python Meetup №81"

        # ссылка на плейлист
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

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
        # количество лайков
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    @property
    def total_duration(self):

        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""

        total_duration = datetime.timedelta(seconds=0)

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):

        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        all_video_like_count = {}

        for video_id in self.video_ids:
            video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                           id=video_id
                                                           ).execute()
            like_count = video_response['items'][0]['statistics']['likeCount']
            all_video_like_count[video_id] = like_count
        id_best_video = max(all_video_like_count, key=lambda k: all_video_like_count[k])
        best_video = "https://youtu.be/" + id_best_video
        return best_video
