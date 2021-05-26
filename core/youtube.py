from core.config import API_KEY_YOUTUBE, COUNT_COMMENTS
from pyyoutube import Api


class YoutubeAPI:
    @staticmethod
    def comments(url: str, limit: int = COUNT_COMMENTS):
        video_id = url.split("v=")[-1]
        api = Api(api_key=API_KEY_YOUTUBE)
        list_of_comments = api.get_comment_threads(video_id=video_id, count=limit)
        messages = list()
        for comment in list_of_comments.items:
            structure = comment.to_dict()
            comment_txt = structure["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            messages.append(comment_txt)
        return messages
