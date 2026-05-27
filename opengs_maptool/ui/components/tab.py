from PyQt6.QtWidgets import QVBoxLayout, QWidget
from opengs_maptool.ui.image_display import ImageDisplay

class Tab(QWidget):
    def __init__(self, tab_name):
        super().__init__()

        # Create image display
        self._image_display = ImageDisplay()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._image_display)

        self._tab_name = tab_name


    def get_image_display(self):
        return self._image_display
    

    def get_tab_name(self):
        return self._tab_name
    