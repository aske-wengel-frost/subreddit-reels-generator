from re import sub
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Story:
    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

def create_database():
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                    (id INTEGER PRIMARY KEY, 
                    title TEXT,
                    body TEXT,
                    author TEXT)''')
    conn.commit() 
    conn.close()

# def retrieve_posts_and_insert_into_database(subreddit_url):
#     # Initialize Chrome webdriver
#     driver = webdriver.Chrome()
#
#     # Open subreddit
#     driver.get(subreddit_url)
#     
#     # Scroll down to load more posts
#     for _ in range(5):  # Scroll down 5 times (you can adjust this number)
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Wait for 2 seconds for posts to load
#
#     # Get post titles
#     posts = driver.find_elements(By.CLASS_NAME, "w-full")
#     
#     conn = sqlite3.connect('reddit_posts.db')
#     cursor = conn.cursor()
#     
#     for post in posts:
#         try:
#             title = post.text.split("ago\n")[1].split("\n")[0]
#             author = post.text.split("\n•")[0].split(title + "\n")[1]
#             body = post.text.split("ago\n")[1].split("\n")[1]
#             story = Story(title, body, author)
#             cursor.execute("INSERT INTO posts (title, body, author) VALUES (?,?,?)", (story.story, story.body, story.author))
#         except Exception as e:
#             print("Not a post..", e)
#     
#     conn.commit()
#     conn.close()
#     driver.close()
#
def retrieve_posts_and_insert_into_database(subreddit_url):
    # Initialize Chrome webdriver
    driver = webdriver.Chrome()

    # Open subreddit
    driver.get(subreddit_url)
    
    # Scroll down to load more posts
    for _ in range(5):  # Scroll down 5 times (you can adjust this number)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for 2 seconds for posts to load

    # Get post titles
    posts = driver.find_elements(By.CLASS_NAME, "w-full")
    
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    
    for post in posts:
        try:
            title = post.text.split("ago\n")[1].split("\n")[0]
            author = post.text.split("\n•")[0].split(title + "\n")[1]
            body = post.text.split("ago\n")[1].split("\n")[1]
            story = Story(title, body, author)
            cursor.execute("INSERT INTO posts (title, body, author) VALUES (?,?,?)", (story.title, story.body, story.author))
        except Exception as e:
            print("Not a post:", e)

    conn.commit()
    conn.close()
    driver.close()

def print_all_data_from_database():
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    for post in posts:
        print(f"Title: {post[1]}")
        print(f"Author: {post[2]}")
        print(f"Body: {post[3]}")

SUBREDDIT_URL = 'https://www.reddit.com/r/RealStories/'

def main():
    create_database()
    retrieve_posts_and_insert_into_database(SUBREDDIT_URL)

if __name__ == "__main__":
    print_all_data_from_database()
"""
    for post in posts:
        try:
            title = post.text.split("ago\n")[1].split("\n")[0]
            author = post.text.split("\n•")[0].split(title + "\n")[1]
            body = post.text.split("ago\n")[1].split("\n")[1]
            story = Story(title, body, author)
            post_titles.append(story)
        except:
            print("not a post")

    # Close the webdriver
    driver.close()
    return post_titles

if __name__ == "__main__":
    subreddit_url = "https://www.reddit.com/r/RealStories/"
    posts = retrieve_posts_and_insert_into_database(subreddit_url)
    # Print retrieved posts
    for i, post in enumerate(posts, start=0):
        print(f"{i}. {post.author} \n {post.title} \n {post.body}\n")

subreddit_url = 'https://www.reddit.com/r/RealStories/'

def get_headers():
    get_post = retrieve_posts(subreddit_url)
    for num, get_post in enumerate(get_post, start=1):
        print(f"{num}. {post.title}")
"""        
