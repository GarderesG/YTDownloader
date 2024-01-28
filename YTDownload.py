from pytube import YouTube
import ffmpeg
import time
import os
import subprocess

class YTDownloader:
    
    def __init__(self, path_with_YT_links):
        self.path_urls = path_with_YT_links

    def download_videos(self):
        """
        Download YT videos from the path provided in __init__
        """
        urls = open(self.path_urls, "r").read().splitlines()

        if len(urls):
            for i, url in enumerate(urls, start=1):
                print(f"Downloading video {i} out of {len(urls)}")
                self.download_video_hq(url)
        else:
            print("No YT url to read from!")
    

    def download_video_hq(self, url: str):
        """
        Separately download highest quality video and audio of YouTube url
        and merge both into mp4 file.
        """
        ti = time.time()

        yt = YouTube(url)
        highest_video_res = max([int(stream.resolution.split("p")[0]) for stream in yt.streams if stream.resolution != None])
        highest_video_res = str(highest_video_res) + "p"

        hq_video_streams = yt.streams.filter(resolution=highest_video_res)

        # mp4 preference if resolution is the same
        hq_video_stream = hq_video_streams[0] if len(hq_video_streams) == 1 else hq_video_streams.filter(subtype="mp4")[0]
        hq_video_stream.download(filename="video.mp4")

        # Download highest res audio
        highest_audio_res = max([int(stream.abr.split("kbps")[0]) for stream in yt.streams.filter(only_audio=True, subtype="mp4")])
        highest_audio_res = str(highest_audio_res) + "kbps"
        
        hq_audio_stream = yt.streams.filter(abr=highest_audio_res)[0]
        hq_audio_stream.download(filename="audio.mp3")

        audio = ffmpeg.input("audio.mp3")
        video = ffmpeg.input("video.mp4")
        #ffmpeg.concat(video, audio).output(yt.title+".mp4").run(overwrite_output=True)

        new_title = yt.title
        if yt.title[0] == "-":
            new_title = yt.title[1:]

        # Remove / from file name    
        ffmpeg.output(audio, video, f"{new_title.replace('/', '_')}.mp4", codec="copy", loglevel="quiet")\
              .run(overwrite_output=True)

        os.remove("video.mp4")
        os.remove("audio.mp3")
        print(f"Download is successful ({time.time()-ti:.2f} seconds)")


if __name__ == "__main__":
    # Download YT urls from file YT_urls.txt
    yt = YTDownloader("YT_urls.txt")
    yt.download_videos()