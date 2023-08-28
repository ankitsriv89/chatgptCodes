"""Write a python code to download any youtube video using tkinter gui. 
the code should show the download progress, failure message and ask for the download location."""

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
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

    def select_location(self):
        self.download_path = filedialog.askdirectory()
        self.location_label.config(text=f"Selected location: {self.download_path}")

    def download(self):
        url = self.url_entry.get()
        try:
            yt = YouTube(url, on_progress_callback=self.show_progress)
            video = yt.streams.get_highest_resolution()
            self.progress_label.config(text="Downloading...")
            video.download(output_path=self.download_path)
            self.progress_label.config(text="Download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.progress_label.config(text="Download failed")

    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_label.config(text=f"Downloading... {percentage:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
