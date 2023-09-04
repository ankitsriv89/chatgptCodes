import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,\
      QHBoxLayout, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot

from pytube import YouTube

class DownloadWorker(QObject):
    finished = pyqtSignal()
    status_update = pyqtSignal(str)

    def __init__(self, urls, download_path, quality):
        super().__init__()
        self.urls = urls
        self.download_path = download_path
        self.quality = quality

    def download_video(self, url):
        try:
            yt = YouTube(url)
            title = yt.title
            self.status_update.emit(f"Downloading: {title}")
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=self.quality).first()
            if stream:
                output_file = os.path.join(self.download_path, f"{title}.mp4")

                """if os.path.isfile(output_file):
                    response = self.confirm_overwrite(title)
                    if response == QMessageBox.No:
                        self.status_update.emit(f"Skipped: {title}")
                        return
                    elif response != QMessageBox.Yes:
                        self.status_update.emit(f"Invalid response. Download canceled for {title}")
                        return"""

                stream.download(output_path=self.download_path)
                self.status_update.emit(f"Downloaded: {title}")
            else:
                self.status_update.emit(f"No video found in {self.quality} quality for {title}")
        except Exception as e:
            self.status_update.emit(f"Error downloading {title}: {str(e)}")

    """def confirm_overwrite(self, title):
        response = QMessageBox.question(None, 'File Exists', f"'{title}.mp4' already exists in the download location. Do you want to replace it?", QMessageBox.Yes | QMessageBox.No)
        return response"""

    def run(self):
        for url in self.urls:
            if url.strip():
                self.download_video(url)
        self.finished.emit()

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Video Downloader')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QHBoxLayout()
        self.sidebar = QVBoxLayout()
        self.video_list = QVBoxLayout()

        self.status_label = QLabel('Download Status')
        self.sidebar.addWidget(self.status_label)

        self.sidebar_status = QTextEdit()
        self.sidebar_status.setReadOnly(True)
        self.sidebar.addWidget(self.sidebar_status)

        self.video_list_label = QLabel('YouTube Video URLs (one per line):')
        self.video_list.addWidget(self.video_list_label)

        self.video_urls = QTextEdit()
        self.video_list.addWidget(self.video_urls)

        self.quality_label = QLabel('Select Quality:')
        self.video_list.addWidget(self.quality_label)

        self.quality = QPushButton('720p')
        self.quality.clicked.connect(self.set_quality)
        self.video_list.addWidget(self.quality)

        self.download_path_label = QLabel('Download Path:')
        self.video_list.addWidget(self.download_path_label)

        self.download_path = QPushButton('Select Folder')
        self.download_path.clicked.connect(self.set_download_path)
        self.video_list.addWidget(self.download_path)

        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.start_download)
        self.video_list.addWidget(self.download_button)

        self.layout.addLayout(self.sidebar)
        self.layout.addLayout(self.video_list)
        self.centralWidget.setLayout(self.layout)

        self.selected_quality = '720p'
        self.selected_download_path = ''

    def set_quality(self):
        quality_options = ['360p', '720p', '1080p']
        selected_quality, ok = QInputDialog.getItem(self, 'Select Quality', 'Select video quality:', quality_options, 0, False)
        if ok:
            self.selected_quality = selected_quality
            self.quality.setText(selected_quality)  # Update the text of the quality button


    def set_download_path(self):
        download_path = QFileDialog.getExistingDirectory(self, 'Select Download Path')
        if download_path:
            self.selected_download_path = download_path

    def start_download(self):
        urls = self.video_urls.toPlainText().split('\n')

        if not self.selected_download_path:
            QMessageBox.warning(self, 'Download Path Not Set', 'Please select a download path.')
            return

        if not urls:
            QMessageBox.warning(self, 'No URLs', 'Please enter YouTube video URLs.')
            return

        self.download_button.setEnabled(False)

        self.worker_thread = threading.Thread(target=self.download_thread, args=(urls,))
        self.worker_thread.start()

    def download_thread(self, urls):
        worker = DownloadWorker(urls, self.selected_download_path, self.selected_quality)
        worker.status_update.connect(self.update_status)
        worker.finished.connect(self.enable_download_button)
        worker.run()

    @pyqtSlot(str)
    def update_status(self, status):
        self.sidebar_status.append(status)

    def enable_download_button(self):
        self.download_button.setEnabled(True)

def main():
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCREEN_SCALE_FACTORS'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
