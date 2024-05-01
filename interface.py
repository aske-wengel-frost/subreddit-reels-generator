from collections.abc import Collection  # Importerer Collection fra collections.abc
from tkinter import ttk, Tk, Listbox, END  # Importerer ttk, Tk, Listbox og END fra tkinter
from get_data import SUBREDDIT_URL, retrieve_posts_and_insert_into_database  # Importerer SUBREDDIT_URL og retrieve_posts_and_insert_into_database fra get_data-modulet
import sqlite3  # Importerer sqlite3-modulet
from os import listdir, path  # Importerer listdir og path fra os-modulet
from get_yt_video import Download  # Importerer Download fra get_yt_video-modulet
from subprocess import Popen  # Importerer Popen fra subprocess-modulet
from custom_exceptions import AgeRestrictedVideoError  # Importerer AgeRestrictedVideoError fra custom_exceptions-modulet
from gtts import gTTS  # Importerer gTTS fra gtts-modulet
import moviepy.editor as mp  # Importerer mp fra moviepy.editor
from moviepy.editor import TextClip, CompositeVideoClip  # Importerer TextClip og CompositeVideoClip fra moviepy.editor

def generate_video_from_selected_content():
    GENERATED_VIDEO_PATH = "./generated_video_files/this_is_a_test2.mp4"  # Stien til den genererede video

    selected_title = return_current_listbox_item()  # Henter den valgte titel fra listen
    if not selected_title:  # Hvis der ikke er valgt nogen titel
        print("No title selected.")  # Udskriver fejlmeddelelse
        return  # Returnerer fra funktionen

    conn = sqlite3.connect("reddit_posts.db")  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en cursor til at udføre SQL-forespørgsler
    cursor.execute("SELECT author, body FROM posts WHERE title=?", (selected_title,))  # Henter forfatter og indhold af posten med den valgte titel
    respective_story_data = cursor.fetchone()  # Henter dataene fra forespørgslen

    if respective_story_data:  # Hvis der er data til den valgte titel
        author, body = respective_story_data  # Udtrækker forfatter og indhold fra dataene
        text = f"Title: {selected_title}\nAuthor: {author}\nStory: {body}"  # Opretter tekst til at inkludere i videoen
        filename = "./generated_video_files/test_output.mp3"  # Filnavn til den genererede lydfil
        text_to_speech(text, filename)  # Konverterer teksten til tale
    else:  # Hvis der ikke er fundet nogen historie i databasen
        print("No story found in database..")  # Udskriver fejlmeddelelse
        conn.close()  # Lukker forbindelsen til databasen
        return  # Returnerer fra funktionen

    selected_video_file = return_current_yt_listbox_item()  # Henter den valgte video fra listen over YouTube-videoer
    path_for_file_video_file = path.abspath(path.join(VIDEO_FILE_PATH, selected_video_file))  # Opretter stien til den valgte video
    if not selected_video_file:  # Hvis der ikke er valgt nogen video
        print("No video file selected.")  # Udskriver fejlmeddelelse
        conn.close()  # Lukker forbindelsen til databasen
        return  # Returnerer fra funktionen
    
    # Indlæser videoklippet
    video_clip = mp.VideoFileClip(path_for_file_video_file)
    
    # Indlæser lydklippet og får dens varighed
    audio_clip = mp.AudioFileClip(filename)
    audio_duration = audio_clip.duration
    
    # Indstiller videoklippets varighed til at matche lydklippets varighed
    video_clip = video_clip.subclip(0, audio_duration)

    # Opretter en TextClip med den ønskede tekst og indstiller dens varighed
    text_clip = TextClip(text, fontsize=None, color='white', bg_color='black', size=(video_clip.size[0], None), method="caption").set_position(('center','top')).set_duration(audio_duration)
    # Sætter tekstklippet og videoklippet sammen
    final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip), text_clip])

    final_clip.write_videofile(GENERATED_VIDEO_PATH, codec='libx264', audio_codec='aac')  # Gemmer den genererede video til en fil
    conn.close()  # Lukker forbindelsen til databasen

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')  # Opretter en gTTS (Google Text-to-Speech) med den angivne tekst og sprog
    tts.save(filename)  # Gemmer talefilen med det angivne filnavn

# Funktion til at kontrollere eksisterende titler i databasen
def check_existing_titles():
    existing_titles = set()  # Opretter en tom sætning for at indeholde eksisterende titler
    conn = sqlite3.connect('reddit_posts.db')  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en cursor til at udføre SQL-forespørgsler
    cursor.execute("SELECT title FROM posts")  # Henter titler fra databasen
    existing_titles.update([title[0] for title in cursor.fetchall()])  # Opdaterer sætningen med de eksisterende titler
    conn.close()  # Lukker forbindelsen til databasen
    return existing_titles  # Returnerer de eksisterende titler

# Funktion til at hente data fra den nuværende database
def get_data_from_current_database():
    listbox.delete(0, "end")  # Rydder listen med titler
    conn = sqlite3.connect('reddit_posts.db')  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en cursor til at udføre SQL-forespørgsler
    cursor.execute("SELECT title FROM posts")  # Henter titler fra databasen
    for title in cursor.fetchall():  # Gennemgår alle titler
        listbox.insert("end", str(title).strip("(''),"))  # Indsætter hver titel i listen
# Funktion til at indlæse nye overskrifter fra Reddit
def load_new_headers():
    listbox.delete(0, END)  # Rydder listen med titler
    current_entry_context = entry_widget.get()  # Henter den aktuelle indtastning fra brugeren
    if current_entry_context == SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT:  # Hvis den aktuelle indtastning er standardteksten for subreddit-URL
        posts = retrieve_posts_and_insert_into_database(SUBREDDIT_URL)  # Henter poster fra standard subreddit-URL
    else:
        posts = retrieve_posts_and_insert_into_database(current_entry_context)  # Henter poster fra den angivne subreddit-URL
    
    if posts:  # Hvis der er poster
        for post in posts:  # Gennemgår hver post
            listbox.insert("end", post.title)  # Indsætter titlen på hver post i listen
    else:  # Hvis der ikke er fundet nogen poster
        listbox.insert("end", "No posts found..")  # Indsætter en meddelelse om, at der ikke blev fundet nogen poster

# Funktion til at returnere den aktuelle valgte titel fra listen
def return_current_listbox_item():
    for i in listbox.curselection():  # Gennemgår alle de valgte elementer i listen
        return listbox.get(i)  # Returnerer den valgte titel

# Funktion til at returnere den aktuelle valgte YouTube-video fra listen
def return_current_yt_listbox_item():
    for i in all_video_files_in_dir_listbox.curselection():  # Gennemgår alle de valgte elementer i YouTube-videoens liste
        return all_video_files_in_dir_listbox.get(i)  # Returnerer den valgte YouTube-video

# Funktion til at slette midlertidig indtastningsbeskrivelse
def delete_temporary_entry_description(event):
    if event.widget == entry_widget and entry_widget.get() == SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT:  # Hvis det aktuelle indtastningsfelt er for subreddit-URL og teksten stadig er standardtekst
        entry_widget.delete(0, "end")  # Sletter teksten i indtastningsfeltet
    elif event.widget == entry_widget_yt_specification and entry_widget_yt_specification.get() == YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT:  # Hvis det aktuelle indtastningsfelt er for YouTube-URL og teksten stadig er standardtekst
        entry_widget_yt_specification.delete(0, "end")  # Sletter teksten i indtastningsfeltet

# Funktion til at genoprette indtastningskonteksten
def restore_entry_context(event):
    if event.widget == entry_widget and not entry_widget.get():  # Hvis det aktuelle indtastningsfelt er tomt for subreddit-URL
        entry_widget.insert(0, SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT)  # Sætter standardteksten tilbage i indtastningsfeltet for subreddit-URL
    elif event.widget == entry_widget_yt_specification and not entry_widget_yt_specification.get():  # Hvis det aktuelle indtastningsfelt er tomt for YouTube-URL
        entry_widget_yt_specification.insert(0, YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT)  # Sætter standardteksten tilbage i indtastningsfeltet for YouTube-URL

# Funktion til at opdatere etiketten for den aktuelle subreddit
def update_current_subreddit_label(event):
    current_entry_context = entry_widget.get()  # Henter den aktuelle indtastning fra brugeren

    if current_entry_context == SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT:  # Hvis den aktuelle indtastning er standardteksten for subreddit-URL
        current_subreddit_label.config(text=f"Current subreddit: {SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT}")  # Opdaterer teksten på etiketten til standard subreddit-URL'en
    else:  # Hvis den aktuelle indtastning ikke er standardteksten for subreddit-URL
        current_subreddit_label.config(text=f"Current subreddit: {current_entry_context}")  # Opdaterer teksten på etiketten til den aktuelle subreddit-URL

# Funktion til at rydde al eksisterende indhold fra databasen
def clear_current_contents_of_database():
    conn = sqlite3.connect("reddit_posts.db")  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en cursor til at udføre SQL-forespørgsler
    cursor.execute("DELETE FROM posts")  # Sletter alle poster fra databasen
    conn.commit()  # Bekræfter ændringerne i databasen
    conn.close()  # Lukker forbindelsen til databasen

# Funktion til at hente forfatter og historie fra den tilsvarende titel og vise dem på brugergrænsefladen
def get_author_and_story_from_respective_title_and_display_on_interface():
    selected_title = return_current_listbox_item()  # Henter den valgte titel fra listen
    if not selected_title:  # Hvis der ikke er valgt nogen titel
        print("No title selected.")  # Udskriver fejlmeddelelse
        return  # Returnerer fra funktionen

    conn = sqlite3.connect("reddit_posts.db")  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en cursor til at udføre SQL-forespørgsler
    cursor.execute("SELECT author, body FROM posts WHERE title=?", (selected_title,))  # Henter forfatter og indhold af posten med den valgte titel
    respective_story_data = cursor.fetchone()  # Henter dataene fra forespørgslen

    if respective_story_data:  # Hvis der er data til den valgte titel
        author, body = respective_story_data  # Udtrækker forfatter og indhold fra dataene
        author_and_story_label.config(text=f"Author: {author}\n\nStory: {body}")  # Opdaterer teksten på etiketten med forfatteren og historien
    else:  # Hvis der ikke er fundet nogen historie i databasen
        author_and_story_label.config(text="No story found in database..")  # Opdaterer teksten på etiketten med en fejlmeddelelse
    conn.close()  # Lukker forbindelsen til databasen

# Funktion til at liste alle aktuelle videofiler
def list_all_current_video_files():
    all_video_files_in_dir_listbox.delete(0, "end")  # Rydder listen med videofiler
    list_of_files_in_path = listdir(VIDEO_FILE_PATH)  # Henter en liste over filer i den angivne sti
    for i in list_of_files_in_path:  # Gennemgår alle filer i stien
        all_video_files_in_dir_listbox.insert("end", i)  # Indsætter hver fil i listen

# Funktion til at hente link og downloade videofil fra YouTube
def fetch_link_and_download_video_file():
    specified_yt_url = entry_widget_yt_specification.get()  # Henter den angivne YouTube-URL fra brugergrænsefladen
    try:
        Download(specified_yt_url)  # Forsøger at downloade videoen fra den angivne URL
    except AgeRestrictedVideoError as e:  # Hvis der opstår en aldersbegrænset video-fejl
        age_restricted_label.config(text=str(e))  # Opdaterer teksten på etiketten med fejlmeddelelsen

# Funktion til at åbne videofil ved valg
def open_video_file_on_selection():
    selected_video_title = return_current_yt_listbox_item()  # Henter den valgte videofil fra listen over YouTube-videoer
    path_for_file_video_file = path.abspath(path.join(VIDEO_FILE_PATH, selected_video_title))  # Opretter stien til den valgte videofil
    try:
        Popen(['open',path_for_file_video_file])  # Åbner den valgte videofil ved hjælp af det relevante program
    except PermissionError as e:  # Hvis der opstår en tilladelsesfejl
        print(f"Permission denied: {e}")  # Udskriver tilladelsesfejlen
    except Exception as e:  # Hvis der opstår en generel fejl
        print(f"Error: {e}")  # Udskriver fejlen

# Stien til den mappe, hvor baggrundsvideoerne er downloadet
VIDEO_FILE_PATH = "./downloaded_background_videoes"
SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT = "Type desired subreddit-URL here.."  # Standardtekst til subreddit-URL
YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT = "Type desired YouTube-URL here.."  # Standardtekst til YouTube-URL
root = Tk()  # Opretter hovedvinduet for GUI'en
frame = ttk.Frame(root, padding=10)  # Opretter en ramme til widget'erne i GUI'en
frame.grid()  # Placerer rammen i hovedvinduet
root.title("YouTube-shorts generator")  # Angiver titlen på hovedvinduet

# Opretter indtastningsfelt til at angive ønsket subreddit
entry_widget = ttk.Entry(frame, width=33)  # Opretter et indtastningsfelt med en bestemt bredde
entry_widget.insert(0, SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT)  # Sætter standardteksten til subreddit-URL'en i indtastningsfeltet
entry_widget.grid(row=0, column=0)  # Placerer indtastningsfeltet i rækken 0 og kolonne 0
entry_widget.bind("<FocusIn>", delete_temporary_entry_description)  # Binder funktionen til at slette midlertidige beskrivelser, når indtastningsfeltet får fokus
entry_widget.bind("<FocusOut>", restore_entry_context)  # Binder funktionen til at genoprette indtastningskonteksten, når indtastningsfeltet mister fokus

current_subreddit_label = ttk.Label(frame, text=f"Current subreddit: {SUBREDDIT_URL}")  # Opretter en etiket til visning af den aktuelle subreddit
current_subreddit_label.grid(row=0, column=1)  # Placerer etiketten i rækken 0 og kolonne 1

ttk.Button(frame, text="Get reddit titles", command=load_new_headers).grid(row=1, column=1)  # Opretter en knap til at hente Reddit-titler og binder den til funktionen for at indlæse nye overskrifter
ttk.Button(frame, text="Get stories from current database", command=get_data_from_current_database).grid(row=0, column=2)  # Opretter en knap til at hente historier fra den aktuelle database og binder den til funktionen for at hente data fra den nuværende database

listbox = Listbox(frame, width=70, height=40, exportselection=0)  # Opretter en liste-widget til visning af Reddit-titler
listbox.grid(row=2, column=1)  # Placerer listen i rækken 2 og kolonne 1

author_and_story_label = ttk.Label(frame, text="", wraplength=300, justify="left")  # Opretter en etiket til visning af forfatter og historie
author_and_story_label.grid(row=2, column=2)  # Placerer etiketten i rækken 2 og kolonne 2
# Button for showing story-data
ttk.Button(frame, text="Show chosen story", command=get_author_and_story_from_respective_title_and_display_on_interface).grid(row=1, column=2)  # Opretter en knap til at vise den valgte historie og binder den til funktionen for at hente forfatter og historie fra den tilsvarende titel og vise dem på brugergrænsefladen

# Allow for clearing all current data from database.
ttk.Button(frame, text="Delete all existing data from databse", command=clear_current_contents_of_database).grid(row=1, column=0)  # Opretter en knap til at slette al eksisterende data fra databasen og binder den til funktionen for at rydde al eksisterende indhold fra databasen

# Listbox for displaying current available video-files.
ttk.Button(frame, text="Show current background-video-files", command=list_all_current_video_files).grid(row=1, column=3)  # Opretter en knap til at vise alle aktuelle baggrundsvideofiler og binder den til funktionen for at liste alle aktuelle videofiler
all_video_files_in_dir_listbox = Listbox(frame, width=40, height=40, exportselection=0)  # Opretter en liste-widget til visning af alle tilgængelige baggrundsvideofiler
all_video_files_in_dir_listbox.grid(row=2, column=3)  # Placerer listen i rækken 2 og kolonne 3

# Buttons for YouTube-background-video related manipulation.
ttk.Button(frame, text="Download video from specified YoutTube-url", command=fetch_link_and_download_video_file).grid(row=1, column=4)  # Opretter en knap til at downloade video fra den angivne YouTube-URL og binder den til funktionen for at hente link og downloade videofil fra YouTube
ttk.Button(frame, text="Open selected video-file", command=open_video_file_on_selection).grid(row=0, column=4)  # Opretter en knap til at åbne den valgte videofil og binder den til funktionen for at åbne videofil ved valg
# Create entry to specifiy desired YouTube-background-video.
entry_widget_yt_specification = ttk.Entry(frame, width=30)  # Opretter et indtastningsfelt til at angive den ønskede YouTube-baggrundsvideo med en bestemt bredde
entry_widget_yt_specification.insert(0, YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT)  # Sætter standardteksten til YouTube-URL'en i indtastningsfeltet
entry_widget_yt_specification.grid(row=0, column=3)  # Placerer indtastningsfeltet i rækken 0 og kolonne 3
entry_widget_yt_specification.bind("<FocusOut>", restore_entry_context)  # Binder funktionen til at genoprette indtastningskonteksten, når indtastningsfeltet mister fokus
entry_widget_yt_specification.bind("<FocusIn>", delete_temporary_entry_description)  # Binder funktionen til at slette midlertidige beskrivelser, når indtastningsfeltet får fokus

# Create the label for displaying age-restricted video error
age_restricted_label = ttk.Label(frame, text="", wraplength=300, justify="left")  # Opretter en etiket til visning af fejlmeddelelsen for aldersbegrænsede videoer
age_restricted_label.grid(row=2, column=0, columnspan=5)  # Placerer etiketten i rækken 2 og kolonne 0 med en bredde på 5 kolonner

# Create button for video-generation.
ttk.Button(frame, text="Create reel from current selection", command=generate_video_from_selected_content).grid(row=4, column=2)  # Opretter en knap til at generere video ud fra den aktuelle markering og binder den til funktionen for at generere video ud fra den aktuelle markering

# Start window-application
root.mainloop()  # Starter hovedloopet for GUI'en

