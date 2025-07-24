import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageFilter, ImageEnhance
import io

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Image Editor")
        self.setGeometry(100, 100, 800, 600)

        self.image = None  # PIL Image
        self.current_image = None  # For display

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Image display
        self.image_label = QLabel("Load an image to start.")
        self.image_label.setFixedSize(600, 400)
        self.image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.image_label)

        # Buttons layout
        btn_layout = QHBoxLayout()

        load_btn = QPushButton("Load Image")
        load_btn.clicked.connect(self.load_image)
        btn_layout.addWidget(load_btn)

        save_btn = QPushButton("Save Image")
        save_btn.clicked.connect(self.save_image)
        btn_layout.addWidget(save_btn)

        grayscale_btn = QPushButton("Grayscale")
        grayscale_btn.clicked.connect(self.apply_grayscale)
        btn_layout.addWidget(grayscale_btn)

        sepia_btn = QPushButton("Sepia")
        sepia_btn.clicked.connect(self.apply_sepia)
        btn_layout.addWidget(sepia_btn)

        blur_btn = QPushButton("Blur")
        blur_btn.clicked.connect(self.apply_blur)
        btn_layout.addWidget(blur_btn)

        brightness_btn = QPushButton("Increase Brightness")
        brightness_btn.clicked.connect(self.increase_brightness)
        btn_layout.addWidget(brightness_btn)

        contrast_btn = QPushButton("Increase Contrast")
        contrast_btn.clicked.connect(self.increase_contrast)
        btn_layout.addWidget(contrast_btn)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_image)
        btn_layout.addWidget(reset_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def save_image(self):
        if self.image:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
            if file_path:
                self.image.save(file_path)
        else:
            QMessageBox.information(self, "No Image", "Please load an image first.")

    def display_image(self, img):
        # Convert PIL image to QPixmap for display
        qimage = self.pil2qimage(img)
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(self.image_label.size())
        self.image_label.setPixmap(scaled_pixmap)
        self.current_image = img

    def pil2qimage(self, pil_image):
        rgb_image = pil_image.convert('RGBA')
        data = rgb_image.tobytes("raw", "RGBA")
        qimage = QImage(data, rgb_image.size[0], rgb_image.size[1], QImage.Format_RGBA8888)
        return qimage

    def apply_grayscale(self):
        if self.image:
            self.image = self.image.convert('L').convert('RGB')
            self.display_image(self.image)

    def apply_sepia(self):
        if self.image:
            sepia_img = self.image.convert('RGB')
            width, height = sepia_img.size
            pixels = sepia_img.load()  # create the pixel map

            for py in range(height):
                for px in range(width):
                    r, g, b = pixels[px, py]

                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    # clamp values
                    r_new = min(255, tr)
                    g_new = min(255, tg)
                    b_new = min(255, tb)

                    pixels[px, py] = (r_new, g_new, b_new)

            self.image = sepia_img
            self.display_image(self.image)

    def apply_blur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.display_image(self.image)

    def increase_brightness(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(1.2)  # Increase brightness by 20%
            self.display_image(self.image)

    def increase_contrast(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(1.2)  # Increase contrast by 20%
            self.display_image(self.image)

    def reset_image(self):
        if self.image:
            self.display_image(self.image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec_())
