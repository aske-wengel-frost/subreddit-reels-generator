from collections.abc import Collection
from tkinter import ttk, Tk, Listbox, END
from get_data import SUBREDDIT_URL, retrieve_posts_and_insert_into_database 
import sqlite3
from os import listdir

def check_existing_titles(posts):
    existing_titles = set()
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM posts")
    existing_titles.update([title[0] for title in cursor.fetchall()])
    conn.close()
    return existing_titles

def get_data_from_current_database():
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

def get_author_and_story_from_respective_title():
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
    path = "/Users/askefrost/Desktop/Programmering/Eksamens projekt/src/downloaded_background_videoes"
    list_of_files_in_path = listdir(path)
    for i in list_of_files_in_path:
        all_video_files_in_dir_listbox.insert("end", i)

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

listbox = Listbox(frame, width=70, height=40)
listbox.grid(row=2, column=1)

author_and_story_label = ttk.Label(frame, text="", wraplength=300, justify="left")
author_and_story_label.grid(row=2, column=2)
# Button for showing story-data
ttk.Button(frame, text="Show chosen story", command=get_author_and_story_from_respective_title).grid(row=1, column=2)

# Allow for clearing all current data from database. 
ttk.Button(frame, text="Delete all existing data from databse", command=clear_current_contents_of_database).grid(row=1, column=0)

# Listbox for displaying current available video-files.
ttk.Button(frame, text="Show current background-video-files", command=list_all_current_video_files).grid(row=1, column=3)
all_video_files_in_dir_listbox = Listbox(frame, width=40, height=40)
all_video_files_in_dir_listbox.grid(row=2, column=3)

ttk.Button(frame, text="Download specified YoutTube-url").grid(row=1, column=4)
# Create entry to specifiy desired YouTube-background-video.
entry_widget_yt_specification = ttk.Entry(frame, width=30)
entry_widget_yt_specification.insert(0, YOUTUBE_URL_SPECIFICTAION_ENTRY_CONTEXT)
entry_widget_yt_specification.grid(row=0, column=3)
entry_widget_yt_specification.bind("<FocusOut>", restore_entry_context)
entry_widget_yt_specification.bind("<FocusIn>", delete_temporary_entry_description)
# Start window-application
root.mainloop()

