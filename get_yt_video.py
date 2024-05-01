from pytube import YouTube
from custom_exceptions import AgeRestrictedVideoError  
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def Download(link: str):
    try:
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        youtubeObject.download(output_path="./downloaded_background_videoes")
        print("Download has completed successfully!")
    except AgeRestrictedVideoError:
        raise AgeRestrictedVideoError("The video is age-restricted and cannot be downloaded.")
    except Exception as e:
        print("An error has occurred:", e)
