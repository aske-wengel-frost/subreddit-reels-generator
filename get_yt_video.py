from pytube import YouTube
import ssl
# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def Download(link:str):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path="./downloaded_background_videoes")
    except Exception as e:
        print("An error has occured", e)
    print("Download has completed sucessfully!")

yt_video_linK = input("Plase enter YouTube-video URL:")
Download(yt_video_linK)
