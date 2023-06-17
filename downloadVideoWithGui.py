import os
import io
import json
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from tkinter import *
from tkinter import filedialog

def download_videos_from_google_photos(start_date, end_date, folder_path):
    # Load Google Photos API credentials from token.json file
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/photoslibrary'])
    # Build Google Photos API client service
    service = build('photoslibrary', 'v1', credentials=creds)

    # Search for all videos in Google Photos library within specified date range
    results = service.mediaItems().search(body={"pageSize": 100, "filters": {"contentFilter": {"includedContentCategories": ["VIDEO"]}, "dateFilter": {"ranges": [{"startDate": f"{start_date}T00:00:00Z", "endDate": f"{end_date}T23:59:59Z"}]}}}).execute()
    items = results.get('mediaItems', [])

    # Download all videos to local directory
    for item in items:
        video_url = item['baseUrl'] + '=dv'
        video_data = requests.get(video_url).content
        with io.open(os.path.join(folder_path, item['filename']), 'wb') as f:
            f.write(video_data)
            print(f"Downloaded {item['filename']}")

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

if __name__ == '__main__':
    # Create GUI window for selecting folder and date range
    root = Tk()
    root.title("Google Photos Video Downloader")
    root.geometry("400x200")

    # Create label and button for selecting folder to save videos locally
    folder_path = StringVar()
    folder_label = Label(root, text="Select folder to save videos:")
    folder_label.pack(pady=10)
    folder_entry = Entry(root, textvariable=folder_path)
    folder_entry.pack(pady=5)
    folder_button = Button(root, text="Browse", command=select_folder)
    folder_button.pack(pady=5)

    # Create label and entry for start date of date range
    start_date_label = Label(root, text="Enter start date (YYYY-MM-DD):")
    start_date_label.pack(pady=10)
    start_date_entry = Entry(root)
    start_date_entry.pack(pady=5)

    # Create label and entry for end date of date range
    end_date_label = Label(root, text="Enter end date (YYYY-MM-DD):")
    end_date_label.pack(pady=10)
    end_date_entry = Entry(root)
    end_date_entry.pack(pady=5)

    # Create button for starting video download process
    #download_button = Button(root, text="Download Videos", command=lambda: download_videos_from_google_photos(start_date_entry.get(), end_date_entry.get(), folder_path.get()))
    #download_button.pack(pady=10)

    root.mainloop()
