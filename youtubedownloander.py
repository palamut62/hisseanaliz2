from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QFileDialog, QProgressBar)
from PyQt6.QtCore import QThread, pyqtSignal
from pytube import YouTube


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, stream, path):
        super().__init__()
        self.stream = stream
        self.path = path

    def run(self):
        self.stream.download(self.path, on_progress_callback=self.on_progress)
        self.finished.emit(self.stream.title)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress.emit(int(percentage_of_completion))


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Video Downloader')

        layout = QVBoxLayout()

        self.url_label = QLabel('Lütfen video URL\'sini girin:')
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        self.download_button = QPushButton('İndir', self)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel('')
        layout.addWidget(self.status_label)

        self.download_button.clicked.connect(self.download_video)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText('Lütfen bir URL girin.')
            return

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            if stream:
                path = QFileDialog.getExistingDirectory(self, "İndirme Konumunu Seçin")
                if path:
                    self.status_label.setText("İndiriliyor...")
                    self.progress_bar.setValue(0)
                    self.download_button.setEnabled(False)
                    self.url_input.setEnabled(False)

                    self.download_thread = DownloadThread(stream, path)
                    self.download_thread.progress.connect(self.progress_bar.setValue)
                    self.download_thread.finished.connect(self.download_finished)
                    self.download_thread.start()
                else:
                    self.status_label.setText('İndirme iptal edildi.')
            else:
                self.status_label.setText('Geçersiz URL veya video bulunamadı.')
        except Exception as e:
            self.status_label.setText('Bir hata oluştu.')

    def download_finished(self, title):
        self.status_label.setText(f"Video '{title}' başarıyla indirildi.")
        self.download_button.setEnabled(True)
        self.url_input.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec())
