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
from PIL import Image
from subprocess import run, PIPE
from re import sub
import tempfile
from io import BytesIO

opts: Dict[str, Any] = {
    "format": "bestvideo+bestaudio/best",
    "noplaylist": False,
    "quiet": True,
    "no_warnings": True,
}


# class Video:
#     """Video Class"""

#     def __init__(self, title: str, length: str, path: str, datetime: str):
#         self.title = title
#         self.length = length
#         self.path = path
#         self.datetime = datetime


class Downloader:
    """Downloader Class"""

    def clean_path(self, path: str) -> str:  # This Base Downloader Class
        """إزالة الرموز غير المدعومة من المسار"""
        return sub(r"[^\w\s.-]", "", path)

    def convert_to_mp4(self, input_path: str) -> str:  # This Base Downloader Class
        """تحويل أي فيديو إلى MP4 بصيغة متوافقة"""
        input_path = os.path.normpath(input_path)
        directory = os.path.dirname(input_path)
        base = os.path.splitext(os.path.basename(input_path))[
            0
        ]  # نأخذ فقط اسم الملف بدون امتداد
        output_path = os.path.join(directory, base + ".mp4")  # نضيف فقط .mp4

        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                output_path,
            ],
            stdout=PIPE,
            stderr=PIPE,
            check=True,
        )
        if os.path.exists(input_path) and input_path != output_path:
            os.remove(input_path)  # نحذف الملف الأصلي
        return output_path

    def set_video_thumbnail(
        self, video_path: str, thumbnail_path: str
    ) -> str:  # This Base Downloader Class
        """إضافة صورة مصغرة للفيديو"""
        video_path = os.path.normpath(video_path)
        thumbnail_path = os.path.normpath(thumbnail_path)

        # لو الامتداد غير مدعوم في attached_pic
        ext = os.path.splitext(video_path)[1].lower()
        if ext not in [".mp4", ".m4a", ".mp3"]:
            video_path = self.convert_to_mp4(video_path)

        # نحتفظ بنفس الاسم ونفس الامتداد
        directory = os.path.dirname(video_path)
        filename = os.path.basename(video_path)
        output_path = os.path.join(directory, filename)

        try:
            command = [
                "ffmpeg",
                "-y",
                "-i",
                video_path,
                "-i",
                thumbnail_path,
                "-map",
                "0",
                "-map",
                "1",
                "-c",
                "copy",
                "-disposition:v:1",
                "attached_pic",
                output_path,
            ]

            run(command, stdout=PIPE, stderr=PIPE, check=True)
            # نحذف الملف المؤقت إذا كان مختلفاً عن النهائي
            if os.path.exists(video_path) and video_path != output_path:
                os.remove(video_path)
            return output_path

        except Exception as e:
            if hasattr(e, "stderr"):
                print(f"FFmpeg error: {e.stderr.decode()}")
            return str(e)

    def YoutubeSearchInfoExtractor(
        self, title: str, max_results: int = 5
    ) -> List[Dict[str, Any]]:  # This Base Downloader Class
        raw_result: Any = YoutubeSearch(title, max_results=max_results).to_dict()

        return raw_result

    def download_thumbnail(
        self, thumbnail_url: str, save_path: str, thumbnail_name="thumbnail"
    ) -> None:  # This Base Downloader Class
        """Downloads thumbnail from URL"""
        try:
            response = get(thumbnail_url, stream=True)
            image = Image.open(BytesIO(response.content))
            ext = image.format.lower()
            image_save_path = os.path.join(
                save_path, "{}.{}".format(thumbnail_name.split(".")[0], ext)
            )
            with open(image_save_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return image_save_path
        except Exception as e:
            return f"Failed to download thumbnail: {e}"

    def check_url(
        self, user_url: str
    ) -> Union[str, Tuple[str, Exception], bool]:  # This Base Downloader Class
        """Checks if URL is reachable"""
        try:
            page = get(user_url)  # type: ignore
            if page.status_code == 200:
                return user_url
            else:
                return False
        except Exception as e:
            return (
                "Error or wrong URL. Check your internet connection and try again.",
                e,
            )

    def path_validator(
        self, path: str
    ) -> Tuple[bool, str]:  # This Base Downloader Class
        """Validates if the given path is a writable directory"""
        if not os.path.exists(path):
            return False, "❌ المجلد غير موجود."
        if not os.path.isdir(path):
            return False, "❌ المسار يشير إلى ملف، مش مجلد."
        if not os.access(path, os.W_OK):
            return False, "❌ لا توجد صلاحية للكتابة هنا."
        return True, "✅ المسار صالح وجاهز للاستخدام."

    def show_history(cls) -> List[Dict[str, Any]]:
        if self.__class__ is not Downloader:
            raise RuntimeError(
                "This method cannot be inherited Use the specific class method in Your Class."
            )
        data = import_data("downloads")
        return cast(List[Dict[str, Any]], data)


class VideoDownloader(Downloader):
    """Video Downloader Class"""

    def __init__(self) -> None:
        super().__init__()

    def get_video_info(
        self, url: str, download_or_not: bool = False
    ) -> Dict[str, Any]:  # This Video Downloader Class
        """Gets video information without downloading"""
        ydl_opts: Dict[str, Any] = {"quiet": True, "skip_download": True}
        with YoutubeDL(ydl_opts):
            info: Any = YoutubeDL(ydl_opts).extract_info(url, download=download_or_not)
        return cast(Dict[str, Any], info)

    @classmethod
    def show_downloaded_history(cls):

        data = import_data("downloads", condition="type='Video'")
        return cast(List[Dict[str, Any]], data)

    def download_video(self, file_path: str, url: str) -> None:
        if self.check_url(url) is False:
            return "The URL is not reachable."
        if self.path_validator(file_path)[0] is False:
            return "The file path is not reachable."

        video_info = self.get_video_info(url)
        video_title = video_info.get("title", "video")
        video_ext = video_info.get("ext", "mp4")

        # تنظيف اسم الملف من أي أحرف غير مدعومة
        video_title = self.clean_path(video_title)
        video_path = os.path.join(file_path, f"{video_title}.{video_ext}")

        local_opts = opts.copy()
        local_opts["outtmpl"] = video_path
        try:
            with YoutubeDL(local_opts) as ytd:
                ytd.download([url])
                # حفظ الصورة المصغرة
                thumbnail_url = video_info.get("thumbnail")
                if thumbnail_url:
                    photo_path = self.download_thumbnail(
                        thumbnail_url,
                        file_path,
                        video_title,  # نستخدم نفس اسم الفيديو للصورة
                    )
                    self.set_video_thumbnail(video_path, photo_path)

                inserting_data(
                    "downloads",
                    "(title,type,url,file_path)",
                    (video_title, "Video", url, video_path),
                )
                return "تم التحميل بنجاح"
        except utils.DownloadError as e:
            return f"Download failed: {e}"


class AudioDownloader(Downloader):
    """Audio Downloader Class"""

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def show_downloaded_history(cls):

        data = import_data("downloads", condition="type='Audio'")
        return cast(List[Dict[str, Any]], data)

    def download_audio(
        self, local_opts: Dict[str, Any], audio_url: str, audio_path: str
    ) -> None:
        opts_copy = local_opts.copy()
        opts_copy["format"] = "bestaudio"
        opts_copy["outtmpl"] = os.path.join(audio_path, "%(title)s.%(ext)s")
        try:
            with YoutubeDL(opts_copy) as ytd:  # type: ignore
                ytd.download([audio_url])
                inserting_data(
                    "downloads",
                    "(title,type,url,file_path)",
                    ("%(title)%.%(ext)s", "Audio", audio_url, audio_path),
                )
        except utils.DownloadError as e:
            print("Download failed:", e)


example_downloader = VideoDownloader()

print(
    example_downloader.download_video(
        "C:\\Users\\Mazen\\Desktop",
        "https://www.youtube.com"
        + example_downloader.YoutubeSearchInfoExtractor("ولا يخاف عقابها ياسر ممدوح")[
            0
        ]["url_suffix"],
    )
)
