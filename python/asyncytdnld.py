"""Write an async python code to download multiple youtube videos using tkinter gui. 
the code should show the download progress, failure message and ask for the download location.
add codes in above program to measure and show download time taken after completion.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import asyncio
import time
from pytube import YouTube

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")

        self.url_label = tk.Label(root, text="Enter YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root)
        self.url_entry.pack()

        self.location_label = tk.Label(root, text="Select download location:")
        self.location_label.pack()

        self.location_button = tk.Button(root, text="Browse", command=self.select_location)
        self.location_button.pack()

        self.download_button = tk.Button(root, text="Download", command=self.download)
        self.download_button.pack()

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack()

        self.time_label = tk.Label(root, text="")
        self.time_label.pack()

    def select_location(self):
        self.download_path = filedialog.askdirectory()
        self.location_label.config(text=f"Selected location: {self.download_path}")

    async def download_video(self, url):
        start_time = time.time()
        try:
            yt = await asyncio.to_thread(YouTube, url)
            video = yt.streams.get_highest_resolution()
            self.progress_label.config(text=f"Downloading {yt.title}...")
            await asyncio.to_thread(video.download, output_path=self.download_path)
            end_time = time.time()
            self.progress_label.config(text=f"Downloaded {yt.title}")
            download_time = end_time - start_time
            self.time_label.config(text=f"Download time: {download_time:.2f} seconds")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.progress_label.config(text=f"Download failed: {e}")

    def download(self):
        url = self.url_entry.get()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download_video(url))

    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_label.config(text=f"Downloading... {percentage:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
