from re import sub  # Importerer sub-funktionen fra re-modulet til regulære udtryk
import sqlite3  # Importerer sqlite3-modulet til at arbejde med SQLite-databaser
from selenium import webdriver  # Importerer webdriver fra Selenium til at automatisere webbrowserhandling
from selenium.webdriver.common.by import By  # Importerer By-klassen fra Selenium til at vælge HTML-elementer efter forskellige kriterier
import time  # Importerer time-modulet til at tilføje forsinkelser

# Definition af Story-klassen til at repræsentere Reddit-posts
class Story:
    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

# Funktion til at oprette SQLite-database, hvis den ikke eksisterer
def create_database():
    conn = sqlite3.connect('reddit_posts.db')  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en databasecursor
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                    (id INTEGER PRIMARY KEY, 
                    title TEXT,
                    body TEXT,
                    author TEXT)''')  # Opretter en tabel 'posts', hvis den ikke allerede eksisterer
    conn.commit()  # Bekræfter ændringerne i databasen
    conn.close()  # Lukker forbindelsen til databasen

# Funktion til at hente Reddit-posts fra et givet subreddit og indsætte dem i databasen
def retrieve_posts_and_insert_into_database(subreddit_url):
    # Initialisering af Chrome webdriver
    driver = webdriver.Chrome()

    # Åbner subreddit i browseren
    driver.get(subreddit_url)
    
    # Scroller ned for at indlæse flere indlæg
    for _ in range(5):  # Scroller ned 5 gange (du kan justere dette tal)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Udfører JavaScript for at scrolle ned til bunden af siden
        time.sleep(2)  # Venter 2 sekunder for at lade indlæggene indlæses

    # Finder indlægstitler
    posts = driver.find_elements(By.CLASS_NAME, "w-full")
    
    conn = sqlite3.connect('reddit_posts.db')  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en databasecursor
    
    for post in posts:
        try:
            title = post.text.split("ago\n")[1].split("\n")[0]  # Ekstraherer titlen fra postens tekst
            author = post.text.split("\n•")[0].split(title + "\n")[1]  # Ekstraherer forfatteren fra postens tekst
            body = post.text.split("ago\n")[1].split("\n")[1]  # Ekstraherer brødteksten fra postens tekst
            story = Story(title, body, author)  # Opretter et Story-objekt med de ekstraherede oplysninger
            cursor.execute("INSERT INTO posts (title, body, author) VALUES (?,?,?)", (story.title, story.body, story.author))  # Indsætter posten i databasen
        except Exception as e:
            print("Not a post:", e)

    conn.commit()  # Bekræfter ændringerne i databasen
    conn.close()  # Lukker forbindelsen til databasen
    driver.close()  # Lukker webbrowseren

# Funktion til at udskrive alle data fra databasen
def print_all_data_from_database():
    conn = sqlite3.connect('reddit_posts.db')  # Opretter forbindelse til SQLite-databasen
    cursor = conn.cursor()  # Opretter en databasecursor
    cursor.execute("SELECT * FROM posts")  # Udfører en SELECT-forespørgsel for at hente alle rækker fra 'posts'-tabellen
    posts = cursor.fetchall()  # Henter alle rækker fra forespørgslen

    for post in posts:
        print(f"Title: {post[1]}")  # Udskriver titlen på posten
        print(f"Author: {post[2]}")  # Udskriver forfatteren af posten
        print(f"Body: {post[3]}")  # Udskriver brødteksten af posten

SUBREDDIT_URL = 'https://www.reddit.com/r/RealStories/'  # URL'en til det ønskede subreddit

def main():
    create_database()  # Opretter SQLite-databasen, hvis den ikke allerede eksisterer
    retrieve_posts_and_insert_into_database(SUBREDDIT_URL)  # Henter og indsætter Reddit-posts i databasen

if __name__ == "__main__":
    print_all_data_from_database()  # Udskriver alle data fra databasen, når scriptet køres direkte

