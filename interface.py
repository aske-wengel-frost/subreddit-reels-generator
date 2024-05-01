from collections.abc import Collection
from tkinter import ttk, Tk, Listbox, END
from get_data import SUBREDDIT_URL, retrieve_posts_and_insert_into_database 
import sqlite3
from os import listdir, path 
from get_yt_video import Download
from subprocess import Popen
from custom_exceptions import AgeRestrictedVideoError
from gtts import gTTS
import moviepy.editor as mp 
from moviepy.editor import TextClip, CompositeVideoClip

from moviepy.editor import TextClip, CompositeVideoClip

def generate_video_from_selected_content():
    GENERATED_VIDEO_PATH = "./generated_video_files/this_is_a_test2.mp4"

    selected_title = return_current_listbox_item()
    if not selected_title:
        print("No title selected.")
        return

    conn = sqlite3.connect("reddit_posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author, body FROM posts WHERE title=?", (selected_title,))
    respective_story_data = cursor.fetchone()

    if respective_story_data:
        author, body = respective_story_data
        text = f"Title: {selected_title}\nAuthor: {author}\nStory: {body}"
        filename = "./generated_video_files/test_output.mp3"
        text_to_speech(text, filename)
    else:
        print("No story found in database..")
        conn.close()
        return

    selected_video_file = return_current_yt_listbox_item()
    path_for_file_video_file = path.abspath(path.join(VIDEO_FILE_PATH, selected_video_file))
    if not selected_video_file:
        print("No video file selected.")
        conn.close()
        return
    
    # Load the video clip
    video_clip = mp.VideoFileClip(path_for_file_video_file)
    
    # Load the audio clip and get its duration
    audio_clip = mp.AudioFileClip(filename)
    audio_duration = audio_clip.duration
    
    # Set the duration of the video clip to match the duration of the audio clip
    video_clip = video_clip.subclip(0, audio_duration)

    # Create a TextClip with the desired text and set its duration
    text_clip = TextClip(text, fontsize=None, color='white', bg_color='black', size=(video_clip.size[0], None), method="caption").set_position(('center','top')).set_duration(audio_duration)
    # Composite the text clip and the video clip
    final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip), text_clip])

    final_clip.write_videofile(GENERATED_VIDEO_PATH, codec='libx264', audio_codec='aac')
    conn.close()

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en') 
    tts.save(filename)

def check_existing_titles():
    existing_titles = set()
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM posts")
    existing_titles.update([title[0] for title in cursor.fetchall()])
    conn.close()
    return existing_titles

def get_data_from_current_database():
    listbox.delete(0, "end")
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM posts")
    for title in cursor.fetchall():
        listbox.insert("end", str(title).strip("(''),"))

def load_new_headers():
    listbox.delete(0, END)
    current_entry_context = entry_widget.get()
    if current_entry_context == SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT: 
        posts = retrieve_posts_and_insert_into_database(SUBREDDIT_URL)
    else:
        posts = retrieve_posts_and_insert_into_database(current_entry_context)
        
    if posts:
        for post in posts:
            listbox.insert("end", post.title)
    else:
        listbox.insert("end", "No posts found..")

def return_current_listbox_item():
    for i in listbox.curselection():
        return listbox.get(i)

def return_current_yt_listbox_item():
    for i in all_video_files_in_dir_listbox.curselection():
        return all_video_files_in_dir_listbox.get(i)

def delete_temporary_entry_description(event):
    if event.widget == entry_widget and entry_widget.get() == SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT:
        entry_widget.delete(0, "end")
    elif event.widget == entry_widget_yt_specification and entry_widget_yt_specification.get() == YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT:
        entry_widget_yt_specification.delete(0, "end")

def restore_entry_context(event):
    if event.widget == entry_widget and not entry_widget.get():
        entry_widget.insert(0, SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT)
    elif event.widget == entry_widget_yt_specification and not entry_widget_yt_specification.get():
        entry_widget_yt_specification.insert(0, YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT)

def update_current_subreddit_label(event):
    # Logic for display the current subreddit shown.
    current_entry_context = entry_widget.get()

    if current_entry_context == SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT:
        current_subreddit_label.config(text=f"Current subreddit: {SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT}")     
    else:
        current_subreddit_label.config(text=f"Current subreddit: {current_entry_context}")

def clear_current_contents_of_database():
    conn = sqlite3.connect("reddit_posts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts")
    conn.commit()
    conn.close()

def get_author_and_story_from_respective_title_and_display_on_interface():
    selected_title = return_current_listbox_item()
    if not selected_title:
        print("No title selected.")
        return

    conn = sqlite3.connect("reddit_posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author, body FROM posts WHERE title=?", (selected_title,))
    respective_story_data = cursor.fetchone()

    if respective_story_data:
        author, body = respective_story_data
        author_and_story_label.config(text=f"Author: {author}\n\nStory: {body}")
    else:
        author_and_story_label.config(text="No story found in database..")
    conn.close()

def list_all_current_video_files():
    all_video_files_in_dir_listbox.delete(0, "end")
    list_of_files_in_path = listdir(VIDEO_FILE_PATH)
    for i in list_of_files_in_path:
        all_video_files_in_dir_listbox.insert("end", i)

def fetch_link_and_download_video_file():
    
    specified_yt_url = entry_widget_yt_specification.get()
    try:
        Download(specified_yt_url)
    except AgeRestrictedVideoError as e:
        age_restricted_label.config(text=str(e))

def open_video_file_on_selection():
    selected_video_title = return_current_yt_listbox_item()
    path_for_file_video_file = path.abspath(path.join(VIDEO_FILE_PATH, selected_video_title))
    try:
        Popen(['open',path_for_file_video_file])
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error: {e}")


VIDEO_FILE_PATH = "./downloaded_background_videoes"
SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT = "Type desired subreddit-URL here.."
YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT = "Type desired YouTube-URL here.."
root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()
root.title("YouTube-shorts generator")

# Create entry to specify desired subreddit.
entry_widget = ttk.Entry(frame, width=33)
entry_widget.insert(0, SUBREDDIT_URL_SPECIFICATION_ENTRY_CONTEXT)
entry_widget.grid(row=0, column=0)
entry_widget.bind("<FocusIn>", delete_temporary_entry_description)
entry_widget.bind("<FocusOut>", restore_entry_context)

current_subreddit_label = ttk.Label(frame, text=f"Current subreddit: {SUBREDDIT_URL}")
current_subreddit_label.grid(row=0, column=1)

ttk.Button(frame, text="Get reddit titles", command=load_new_headers).grid(row=1, column=1)
ttk.Button(frame, text="Get stories from current database", command=get_data_from_current_database).grid(row=0, column=2)

listbox = Listbox(frame, width=70, height=40, exportselection=0)
listbox.grid(row=2, column=1)

author_and_story_label = ttk.Label(frame, text="", wraplength=300, justify="left")
author_and_story_label.grid(row=2, column=2)
# Button for showing story-data
ttk.Button(frame, text="Show chosen story", command=get_author_and_story_from_respective_title_and_display_on_interface).grid(row=1, column=2)

# Allow for clearing all current data from database. 
ttk.Button(frame, text="Delete all existing data from databse", command=clear_current_contents_of_database).grid(row=1, column=0)

# Listbox for displaying current available video-files.
ttk.Button(frame, text="Show current background-video-files", command=list_all_current_video_files).grid(row=1, column=3)
all_video_files_in_dir_listbox = Listbox(frame, width=40, height=40, exportselection=0)
all_video_files_in_dir_listbox.grid(row=2, column=3)

# Buttons for YouTube-background-video related manipulation.
ttk.Button(frame, text="Download video from specified YoutTube-url", command=fetch_link_and_download_video_file).grid(row=1, column=4)
ttk.Button(frame, text="Open selected video-file", command=open_video_file_on_selection).grid(row=0, column=4)
# Create entry to specifiy desired YouTube-background-video.
entry_widget_yt_specification = ttk.Entry(frame, width=30)
entry_widget_yt_specification.insert(0, YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT)
entry_widget_yt_specification.grid(row=0, column=3)
entry_widget_yt_specification.bind("<FocusOut>", restore_entry_context)
entry_widget_yt_specification.bind("<FocusIn>", delete_temporary_entry_description)

# Create the label for displaying age-restricted video error
age_restricted_label = ttk.Label(frame, text="", wraplength=300, justify="left")
age_restricted_label.grid(row=2, column=0, columnspan=5)

# Create button for video-generation.
ttk.Button(frame, text="Create reel from current selection", command=generate_video_from_selected_content).grid(row=4, column=2)
# Start window-application
root.mainloop()
