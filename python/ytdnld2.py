import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pytube import YouTube
import threading
import tkinter.filedialog


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        self.url_label = tk.Label(root, text="Enter YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root)
        self.url_entry.pack()

        self.location_label = tk.Label(root, text="Choose download location:")
        self.location_label.pack()

        self.location_button = tk.Button(root, text="Browse", command=self.choose_location)
        self.location_button.pack()

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack()

        self.download_button = tk.Button(root, text="Download", command=self.start_download)
        self.download_button.pack()

    def choose_location(self):
        self.download_location = tk.filedialog.askdirectory()
    
    def update_progress(self, stream, chunk, file_handle, bytes_remaining):
        percent = int(((stream.filesize - bytes_remaining) / stream.filesize) * 100)
        self.progress["value"] = percent
        self.root.update_idletasks()

    def download_complete(self):
        messagebox.showinfo("Download Complete", "Video downloaded successfully!")

    def download_failure(self):
        messagebox.showerror("Download Error", "Failed to download the video.")

    def download_video(self):
        try:
            yt = YouTube(self.url_entry.get(), on_progress_callback=self.update_progress)
            stream = yt.streams.get_highest_resolution()
            stream.download(self.download_location)
            self.download_complete()
        except:
            self.download_failure()

    def start_download(self):
        if not hasattr(self, 'download_location'):
            messagebox.showerror("Download Error", "Please choose a download location.")
            return

        download_thread = threading.Thread(target=self.download_video)
        download_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
