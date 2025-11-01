"""
This File For Downloading Media From Internet
"""

# ---------------------------------------------------------------------------
# -------------------------- Downloader Manager Back-End -------------------
# ---------------------------------------------------------------------------

from databass_conection import inserting_data, import_data
from youtube_search import YoutubeSearch  # type: ignore
from yt_dlp import YoutubeDL, utils
from requests import get
import os
from typing import Any, cast, Dict, List, Union, Tuple


opts: Dict[str, Any] = {
    "format": "bestvideo+bestaudio/best",
    "noplaylist": False,
    "quiet": True,
    "no_warnings": True,
}


class Video:
    """Video Class"""

    def __init__(self, title: str, length: str, path: str, datetime: str):
        self.title = title
        self.length = length
        self.path = path
        self.datetime = datetime


class Downloader:
    """Downloader Class"""


    from typing import Any, cast, List, Dict

    def YoutubeSearchInfoExtractor(self, title: str, max_results: int = 5) -> List[Dict[str, Any]]:
        raw_result: Any = YoutubeSearch(title, max_results=max_results).to_dict()
        if isinstance(raw_result, list):
            # نؤكد للـ type checker إن ده List[Dict[str, Any]]
            return cast(List[Dict[str, Any]], raw_result)
        # لو حاجة تانية اتعرضت، نرجع قائمة فاضية بدل str
        return []


    def get_video_info(self, url: str) -> Dict[str, Any]:
        ydl_opts: Dict[str, Any] = {"quiet": True, "skip_download": True}
        with YoutubeDL(ydl_opts):  # type: ignore
            info: Any = YoutubeDL(ydl_opts).extract_info(url, download=False)  # type: ignore
        return cast(Dict[str, Any], info)

    def check_url(self, user_url: str) -> Union[str, Tuple[str, Exception], bool]:
        """Checks if URL is reachable"""
        try:
            page = get(user_url)  # type: ignore
            if page.status_code == 200:
                return user_url
            else:
                return False
        except Exception as e:
            return ("Error or wrong URL. Check your internet connection and try again.", e)

    def path_validator(self, path: str) -> Tuple[bool, str]:
        if not os.path.exists(path):
            return False, "❌ المجلد غير موجود."
        if not os.path.isdir(path):
            return False, "❌ المسار يشير إلى ملف، مش مجلد."
        if not os.access(path, os.W_OK):
            return False, "❌ لا توجد صلاحية للكتابة هنا."
        return True, "✅ المسار صالح وجاهز للاستخدام."

    def download_video(self, file_path: str, url: str) -> None:
        if self.check_url(url) is False:
            return
        if self.path_validator(file_path)[0] is False:
            return

        video_info = self.get_video_info(url)
        video_path = os.path.join(file_path, video_info.get("title", "video"))

        local_opts = opts.copy()
        local_opts["outtmpl"] = video_path
        try:
            with YoutubeDL(local_opts) as ytd:  # type: ignore
                info: Any = ytd.extract_info(url, download=True)  # type: ignore
                respone = get(info.get("thumbnail"))  # type: ignore
                inserting_data(
                    "downloads",
                    "(title,type,url,file_path)",
                    (info.get("title", "unknown"), "Video", url, video_path),
                )
            # Save thumbnail
            thumb_file = os.path.join(file_path, f"{info.get('title','video')}.jpg")
            with open(thumb_file, "wb") as f:
                f.write(respone.content)
                inserting_data("downloads", "(thumbnail)", (thumb_file,))
        except utils.DownloadError as e:
            print("Download failed:", e)

    def download_audio(self, local_opts: Dict[str, Any], audio_url: str, audio_path: str) -> None:
        opts_copy = local_opts.copy()
        opts_copy["format"] = "bestaudio"
        opts_copy["outtmpl"] = os.path.join(audio_path, "%(title)s.%(ext)s")
        try:
            with YoutubeDL(opts_copy) as ytd:  # type: ignore
                ytd.download([audio_url])
                inserting_data(
                    "downloads",
                    "(title,type,url,file_path)",
                    ("%TITLE%.%(ext)s", "Audio", audio_url, audio_path),
                )
        except utils.DownloadError as e:
            print("Download failed:", e)

    @classmethod
    def show_history(cls) -> List[Dict[str, Any]]:
        data = import_data("downloads")
        return cast(List[Dict[str, Any]], data)


# Example Usage
example = Downloader()
print(example.path_validator("C:"))
