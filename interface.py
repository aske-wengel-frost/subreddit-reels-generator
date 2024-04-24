from tkinter import ttk, Tk, Listbox, END
from get_data import SUBREDDIT_URL, retrieve_posts_and_insert_into_database 
import sqlite3

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
    if current_entry_context == ENTRY_CONTEXT: 
        posts = retrieve_posts_and_insert_into_database(SUBREDDIT_URL)
    else:
        posts = retrieve_posts_and_insert_into_database(current_entry_context)
        
    if posts:
        for post in posts:
            listbox.insert("end", post.title)
    else:
        listbox.insert("end", "No posts found..")

def return_current_listbox():
    for i in listbox.curselection():
        print(listbox.get(i))

def delete_temporary_entry_description(entry):
    entry_widget.delete(0, "end")

def update_current_subreddit_label(event):
    # Logic for display the current subreddit shown.
    current_entry_context = entry_widget.get()

    if current_entry_context == ENTRY_CONTEXT:
        current_subreddit_label.config(text=f"Current subreddit: {ENTRY_CONTEXT}")     
    else:
        current_subreddit_label.config(text=f"Current subreddit: {current_entry_context}")

def clear_current_contents_of_database():
    conn = sqlite3.connect("reddit_posts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts")
    conn.commit()
    conn.close()

root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()
root.title("YouTube-shorts generator")


ENTRY_CONTEXT = "Type desired subreddit-URL here.."
# Create entry to specify desired subreddit.
entry_widget = ttk.Entry(frame, width=33)
entry_widget.insert(0, ENTRY_CONTEXT)
entry_widget.grid(row=0, column=0)
entry_widget.bind("<FocusIn>", delete_temporary_entry_description)
entry_widget.bind("<FocusOut>", update_current_subreddit_label)

current_subreddit_label = ttk.Label(frame, text=f"Current subreddit: {SUBREDDIT_URL}")
current_subreddit_label.grid(row=0, column=1)

ttk.Button(frame, text="Get reddit titles", command=load_new_headers).grid(row=1, column=1)

ttk.Button(frame, text="Get stories from current database", command=get_data_from_current_database).grid(row=0, column=2)
listbox = Listbox(frame, width=100, height=40)
listbox.grid(row=2, column=1)

# Button for showing story-data
ttk.Button(frame, text="Show chosen story", command=return_current_listbox).grid(row=1, column=2)

# Allow for clearing all current data from database. 
ttk.Button(frame, text="Delete all existing data from databse", command=clear_current_contents_of_database).grid(row=1, column=0)
# Start window-application
root.mainloop()

