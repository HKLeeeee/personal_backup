from pytube import Playlist, YouTube
from moviepy.video.VideoClip import * ## moviepy<=1.0.2
from moviepy.audio.AudioClip import *
from moviepy.editor import *

# video data
class YoutubeCrawling:
    # 출처: https://butnotforme.tistory.com/entry/파이썬으로-유튜브-고화질-영상-다운로드-하기 [butnotforme:티스토리]
    def __init__(self):
        self.fpath = lambda x: '../data/' + x
        self.output_path = '../data/youtube'

    def ydown(self, url: str, prefix: str = ""):
        yt = YouTube(url)
        # yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first().download(output_path=output_path, filename_prefix=f"{prefix} ")

        vpath = (
            yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True)
            .order_by("resolution")
            .desc()
            .first()
            .download(output_path=self.fpath("youtube_video/"), filename_prefix=f"{prefix} ")
        )
        apath = (
            yt.streams.filter(adaptive=True, file_extension="mp4", only_audio=True)
            .order_by("abr")
            .desc()
            .first()
            .download(output_path=self.fpath("youtube_audio/"), filename_prefix=f"{prefix} ")
        )

        v = VideoFileClip(vpath)
        a = AudioFileClip(apath)

        v.audio = a
        print(v.fps)
        v.write_videofile(self.fpath(f"youtube/{vpath.split('/')[-1]}"), fps=v.fps)

    #     v.download(DOWNLOAD_FOLDER)

    def playlistdown(self, url: str, prefix: str = ""):
        pl = Playlist(url)

        for v in pl.video_urls:
            try:
                self.ydown(v, prefix)
            except Exception as e:
                print(e)
                continue
