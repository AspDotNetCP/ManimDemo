from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt,QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PIL import Image
import tkinter as tk
import os
import sys

class AnimationWidget(QWidget):
    def __init__(self, frames, delay, parent=None):
        super().__init__(parent)
        self.frames = frames
        self.delay = delay
        self.index = 0
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Remove window decorations and make the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)  # Transparent background
        self.setWindowFlags(Qt.FramelessWindowHint)  # No border or title bar

        # Set window size to match the animation size
        self.setFixedSize(QSize(frames[0].width, frames[0].height))

        # Timer for frame update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.delay)

    def update_frame(self):
        if self.index < len(self.frames):
            frame = self.frames[self.index]
            if isinstance(frame, Image.Image):
                frame = frame.convert("RGBA")
                data = frame.tobytes("raw", "RGBA")
                qimage = QImage(data, frame.width, frame.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimage)
                self.label.setPixmap(pixmap)
                self.index += 1
        else:
            self.index = 0

    def paintEvent(self, event):
        # Ensure that the widget is painted with no background
        painter = QPainter(self)
        painter.setOpacity(1.0)  # Full opacity for the animation layer
        painter.fillRect(self.rect(), Qt.transparent)  # Transparent background for widget

        super().paintEvent(event)

def is_nearly_black(pixel, threshold):
    """Check if a pixel YES nearly black almost totally."""
    return pixel[0] < threshold and pixel[1] < threshold and pixel[2] < threshold

class TkinterThread(QThread):
    # Signal to send data from the Tkinter thread to the main thread
    user_input_signal = pyqtSignal(str)

    def run(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry('300x50+500+300')

        def on_keyrelease(event):
            search_text = entry.get()
            if len(search_text) > 2:
                # Send the search text to the main thread
                self.user_input_signal.emit(search_text)
            else:
                animation_window.hide()

        items = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi"]

        entry = tk.Entry(self.root, font=('Helvetica', 16, 'bold'))
        entry.pack(fill='both', expand=True)
        entry.focus_set()
        entry.bind('<KeyRelease>', on_keyrelease)

        self.root.mainloop()


def load_frames(config):
    folder_path = config['folder_path']
    output_folder = config['output_folder']
    size = config['size']
    threshold = config['threshold']
    filename_prefix = config['filename_prefix']

    frame_files = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".png")]
    )
    frames = []
    for i, f in enumerate(frame_files):
        output_file = os.path.join(output_folder, f"{filename_prefix}{i:04d}.png")
        if os.path.exists(output_file):
            # Load the processed image if it exists
            img = Image.open(output_file).convert("RGBA")
        else:
            # Process the original image
            img = Image.open(f).convert("RGBA")  # Ensure image has an alpha channel
            img = img.resize(size)
            datas = img.getdata()

            # Remove black background
            new_data = []
            for item in datas:
                # Change all nearly black pixels to transparent
                if item[0] < threshold and item[1] < threshold and item[2] < threshold:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)

            # Save the processed image to the output folder
            img.save(output_file)

        frames.append(img)
    return frames


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1200, 1200)

        self.setAttribute(Qt.WA_TranslucentBackground)  # Set transparent background for the window
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window border
        
        self.animation_widget = None
        self.animation_window = None

        # Start Tkinter input in a separate thread
        self.tk_thread = TkinterThread()
        self.tk_thread.user_input_signal.connect(self.show_animation_widget)
        self.tk_thread.start()

    def show_animation_widget(self, search_text):
        items = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi"]
        filtered_items = [item for item in items if search_text.lower() in item.lower()]
        if filtered_items:
            # Load frames generated by Manim
            frames_folder = "C:/Downloads/Labyrinth-of-Fear-3D-main/My_Game/media/images/HelloWorldAndSquareToCircleEllipseRay"  # Update to the correct path
            output_folder = "C:/Downloads/Labyrinth-of-Fear-3D-main/My_Game/media/output_folder"  # Update to the correct path
            filename_prefix = "AnimateEllipsesText_"  # Define the filename prefix
            config = {
                'folder_path': frames_folder,
                'output_folder': output_folder,
                'size': (1200, 1200),
                'threshold': 30,
                'filename_prefix': filename_prefix
            }
            frames = load_frames(config)
            if frames:
                self.animation_widget = AnimationWidget(frames, 100)
                self.setCentralWidget(self.animation_widget)
                self.show()
        else:
            self.hide()


if __name__ == "__main__":
    app = QApplication([])

    # Create main window for PyQt5 animation
    animation_window = MainWindow()

    # Show PyQt5 main window
     # Maximize the main window
    animation_window.showFullScreen()  # Use showMaximized() if you want to consider window decorations

    #animation_window.show()

    app.exec_()  # PyQt event loop
