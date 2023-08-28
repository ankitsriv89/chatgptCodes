"""add code in above program to compute file size to download and prompt user to continue or abort"""


import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
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

        self.download_button = tk.Button(root, text="Download", command=self.confirm_download)
        self.download_button.pack()

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack()

        self.time_label = tk.Label(root, text="")
        self.time_label.pack()

        self.downloading_file = tk.StringVar()
        self.downloading_label = tk.Label(root, textvariable=self.downloading_file)
        self.downloading_label.pack()

    def select_location(self):
        self.download_path = filedialog.askdirectory()
        self.location_label.config(text=f"Selected location: {self.download_path}")

    def compute_file_size(self, url):
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        file_size = video.filesize
        return file_size

    def download_video(self, url):
        start_time = time.time()
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            self.download_button.config(state=tk.DISABLED)
            self.downloading_file.set(f"Downloading: {yt.title}")
            video.download(output_path=self.download_path)
            end_time = time.time()
            self.progress_label.config(text=f"Downloaded {yt.title}")
            download_time = end_time - start_time
            self.time_label.config(text=f"Download time: {download_time:.2f} seconds")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.progress_label.config(text=f"Download failed: {e}")
        finally:
            self.download_button.config(state=tk.NORMAL)
            self.downloading_file.set("")
            self.progress_label.config(text="")

    def confirm_download(self):
        url = self.url_entry.get()
        file_size = self.compute_file_size(url)
        size_mb = file_size / (1024 * 1024)
        response = messagebox.askyesno("Confirmation", f"The video size is approximately {size_mb:.2f} MB.\nDo you want to continue with the download?")
        if response:
            self.download_video(url)
        else:
            messagebox.showinfo("Download Aborted", "Download has been aborted.")

    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_label.config(text=f"Downloading... {percentage:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
