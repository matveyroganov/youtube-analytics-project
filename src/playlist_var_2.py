from src.channel import Channel
from src.video import PLVideo
import datetime
import isodate


class Playlist(PLVideo):
    def __init__(self, playlist_id):
        super().__init__(playlist_id)
        self.title = "Moscow Python Meetup №81"
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    @property
    def total_duration(self):

        total_duration = datetime.timedelta(seconds=0)

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        all_video_like_count = {}

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
