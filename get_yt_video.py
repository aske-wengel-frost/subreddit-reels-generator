from pytube import YouTube  # Importerer YouTube-modulet fra pytube-biblioteket
from custom_exceptions import AgeRestrictedVideoError  # Importerer AgeRestrictedVideoError fra custom_exceptions-modulet
import ssl  # Importerer ssl-modulet til at håndtere SSL-forbindelsesfejl

# Da SSL-fejl kan opstå, oprettes en midlertidig løsning for at deaktivere HTTPS-kontekstkontrol
ssl._create_default_https_context = ssl._create_unverified_context

# Funktion til at downloade video fra YouTube
def Download(link: str):
    try:
        youtubeObject = YouTube(link)  # Opretter et YouTube-objekt ved hjælp af den angivne video-URL
        youtubeObject = youtubeObject.streams.get_highest_resolution()  # Finder den højeste opløsning for videoen
        youtubeObject.download(output_path="./downloaded_background_videoes")  # Downloader videoen til den angivne sti
        print("Download has completed successfully!")  # Udskriver besked om, at download er fuldført
    except AgeRestrictedVideoError:  # Hvis videoen er aldersbegrænset
        raise AgeRestrictedVideoError("The video is age-restricted and cannot be downloaded.")  # Kaster en AgeRestrictedVideoError
    except Exception as e:  # Hvis der opstår en generel fejl under download
        print("An error has occurred:", e)  # Udskriver fejlen

