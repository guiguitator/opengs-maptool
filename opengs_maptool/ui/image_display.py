from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt


class ImageDisplay(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #333")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self._image = None


    def set_image(self, image):
        if image is None:
            self._image = None
            self.clear()
            return

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        self._image = image
        self._update_pixmap()


    def _update_pixmap(self):
        if self._image is None:
            return

        qimage = QImage(
            self._image.tobytes("raw", "RGBA"),
            self._image.width,
            self._image.height,
            QImage.Format.Format_RGBA8888
        )

        pixmap = QPixmap.fromImage(qimage)

        pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(pixmap)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_pixmap()


    def get_image(self):
        return self._image
