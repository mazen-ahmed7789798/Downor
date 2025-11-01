"This File For Downloading Media From Internet"

# ------------------------------------------------------------------------------
# -------------------------- Downloader Manager Back-End -----------------------
# ------------------------------------------------------------------------------

from databass_conection import inserting_data, import_data
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL, utils

from requests import get
import os

test_listUrls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
]
opts = {
    "format": "bestvideo+bestaudio/best",
    "noplaylist": False,
    "quiet": True,
    "no_warnings": True,
}


class Video:
    "This is Video Class"

    def __init__(self, title: str, length: str, path: str, datetime: str):
        self.title = title
        self.length = length
        self.path = path
        self.datetime = datetime


class Downloader:
    "This is Video Class"

    def YoutubeSearchInfoExtractor(self, title : str, max_results : int =5) -> dict:
        results = YoutubeSearch(title, max_results=max_results).to_dict()
        return results

    def get_video_info(self, url: str) -> str:
        ydl_opts = {"quiet": True, "skip_download": True}
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def check_url(self, user_url : str) -> str:
        "This Function Gets Url From The User"
        try:
            page = get(user_url)
            if page.status_code == 200:
                return user_url
            else:
                return False
        except Exception as e:
            return (
                "Error or wrong URL. Check your internet connection and try again.",
                e,
            )

    def path_validator(self, path: str):
        if not os.path.exists(path):
            return False, "❌ المجلد غير موجود."
        if not os.path.isdir(path):
            return False, "❌ المسار يشير إلى ملف، مش مجلد."
        if not os.access(path, os.W_OK):
            return False, "❌ لا توجد صلاحية للكتابة هنا."
        return True, "✅ المسار صالح وجاهز للاستخدام."

    def download_video(self, file_path, url):
        """This Function To Download A Video
        Param  Video_url : This's a Link Of Playlist Page.
        Param  Video_path : This's a Path which Will Playlist Download On It ."""

        # URL Checking
        if self.check_url(url) is False:
            return self.check_url(url)
        url = url
        # Path Checking
        if self.path_validator(file_path) is False:
            return self.path_validator(file_path)
        video_path = file_path
        opts["outtmpl"] = os.path.join(file_path, self.get_video_info(url)["title"])
        # try:
        #     with YoutubeDL(opts) as ytd:
        #         info = ytd.extract_info(url, download=True)
        #         respone = get(info.get("thumbnail"))
        #         inserting_data(
        #             "downlaods",
        #             "(title,type,url,file_path)",
        #             ("".format(info"), "Video", url, video_path),
        #         )
        #     with open(info.get("title") + ".jpg", "wb") as f:
        #         f.write(respone.content)
        #         inserting_data("downloads", "(thumbnail)", (f"{info.get("title")}.jpg",))
        # except utils.DownloadError as e:
        #     print("Download failed:", e)

    def download_audio(self, audio_url: str, audio_path: str):
        """This Function To Download Audio Only
        Param  Audio_url : This's a Link Of Audio Page.
        Param  Audio_path : This's a Path which Will Audio Download in It ."""
        local_opts = opts.copy()
        local_opts["format"] = "bestaudio"
        local_opts["outtmpl"] = "{}\\ %(title)s.%(ext)s".format(audio_path)
        with YoutubeDL(local_opts) as ytd:
            try:
                ytd.download(audio_url)
                inserting_data(
                    "downlaods",
                    "(title,type,url,file_path)",
                    ("%(title)s.%(ext)s", "Audio", audio_url, audio_path),
                )
            except utils.DownloadError as e:
                print("Download failed:", e)

    @classmethod
    def show_histroy(cls):
        data = import_data("downloads")
        return data


example = Downloader()
print(example.path_validator("C:"))

# if __name__ == "__main__":

#     import Downloader_manager
