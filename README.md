# subreddit-reels-generator
This program provides a simple graphical user interface (GUI) built with Tkinter for generating short-videos like reels seen on Instagram or YouTube from given subreddit-posts. It allows users to retrieve posts from a specified subreddit URL, display post titles, view post details, and clear all existing data from the local SQLite database. 

## Features

- Retrieve posts from a specified subreddit URL.
- Display post titles in a listbox.
- View details of selected post including title, body, and author.
- Clear all existing data from the local SQLite database.

## Dependencies

- Python 3.x
- Tkinter
- Selenium
- Chrome webdriver
- SQLite3

## Setup

1. Install the necessary dependencies using pip:
    ```bash
    pip install selenium
    ```

2. Download Chrome webdriver suitable for your platform from [Chrome Driver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads) and make sure it's in your system's PATH.

## Usage

1. Run the program by executing the provided script:
    ```bash
    python interface.py
    ```

2. Once the GUI window opens:
    - Enter the desired subreddit URL in the entry field provided.
    - Click the "Get reddit titles" button to retrieve post titles from the specified subreddit.
    - Click the "Get stories from current database" button to display posts stored in the local database.
    - Select a post title from the listbox to view its details.
    - Click the "Show chosen story" button to print the details of the selected post in the console.
    - Click the "Delete all existing data from database" button to clear all data stored in the local database.

## Interface

The interface is designed to be intuitive and user-friendly, allowing users to easily navigate and interact with the application. It includes the following components:
- Entry widget for specifying the subreddit URL.
- Label widget for displaying the current subreddit.
- Buttons for retrieving post titles, displaying post data, and clearing the database.
- Listbox for displaying post titles retrieved from Reddit.
- Interaction buttons for showing selected post details.

## Future Enhancements

- Implement functionality to retrieve post bodies and authors.
- Add support for selecting video links and preinstalled videos.
- Combine text, reading, and background video to create a single video.

## License

This project is licensed under the [MIT License](LICENSE).
