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
    posts = retrieve_posts_and_insert_into_database(SUBREDDIT_URL)
    
    if posts:
        for post in posts:
            listbox.insert("end", post.title)
        # existing_titles = check_existing_titles(posts)
        # for post in posts:
        #     if post.title not in existing_titles:
        #         listbox.insert("end", post.title)
        #     else:
        #         print(f"Skipping already existing post: {post.title}")
    else:
        listbox.insert("end", "No posts found..")

def return_current_listbox():
    for i in listbox.curselection():
        print(listbox.get(i))

root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()
root.title("YouTube-shorts generator")

current_subreddit = f"Current subreddit: {SUBREDDIT_URL}"
ttk.Label(frame, text=current_subreddit).grid(row=0, column=1)
ttk.Button(frame, text="Get reddit titles", command=load_new_headers).grid(row=1, column=1)

ttk.Button(frame, text="Get stories from current database", command=get_data_from_current_database).grid(row=0, column=2)
listbox = Listbox(frame, width=100, height=40)
listbox.grid(row=2, column=1)

# Button for showing story-data
ttk.Button(frame, text="Show chosen story", command=return_current_listbox).grid(row=1, column=2)

# Start window-application
root.mainloop()

