from pytube import YouTube
import ffmpeg
import time
import os

class YTDownloader:
    
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
        self.download_time = None

    def get_video_name(self):
        """
        Returns name of the You Tube video and apply basic formatting
        """
        clean_title = self.yt.title
        
        # Remove initial dash if any
        if clean_title[0] == "-":
            clean_title = clean_title[1:]

        # Remove unwanted characters
        clean_title = clean_title.replace('/', '_')

        return clean_title

    def get_highest_video_res(self):

        highest_video_res = max([int(stream.resolution.split("p")[0]) for stream in self.yt.streams if stream.resolution != None])
        return str(highest_video_res) + "p"


    def get_highest_audio_res(self):
        
        highest_audio_res = max([int(stream.abr.split("kbps")[0]) for stream in self.yt.streams.filter(only_audio=True, subtype="mp4")])
        return str(highest_audio_res) + "kbps"

    def download_video_hq(self):
        """
        Separately download highest quality video and audio of YouTube url
        and merge both into mp4 file.
        """
        ti = time.time()
        highest_video_res = self.get_highest_video_res()
        hq_video_streams = self.yt.streams.filter(resolution=highest_video_res)

        # mp4 preference if resolution is the same
        hq_video_stream = hq_video_streams[0] if len(hq_video_streams) == 1 else hq_video_streams.filter(subtype="mp4")[0]
        hq_video_stream.download(filename="video.mp4")

        # Download highest res audio
        highest_audio_res = self.get_highest_audio_res()
        
        hq_audio_stream = self.yt.streams.filter(abr=highest_audio_res)[0]
        hq_audio_stream.download(filename="audio.mp3")

        audio = ffmpeg.input("audio.mp3")
        video = ffmpeg.input("video.mp4")
        
        # Remove / from file name    
        ffmpeg.output(audio, video, f"{self.get_video_name()}.mp4", codec="copy", loglevel="quiet")\
              .run(overwrite_output=True)

        os.remove("video.mp4")
        os.remove("audio.mp3")
        
        self.download_time = time.time()-ti