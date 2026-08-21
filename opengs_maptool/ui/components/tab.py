from PyQt6.QtWidgets import QVBoxLayout, QWidget
from opengs_maptool.simple_types import TabName
from opengs_maptool.ui.image_display import ImageDisplay

class Tab(QWidget):
    def __init__(self, tab_name_enum: TabName):
        super().__init__()

        # Create image display
        self._image_display = ImageDisplay()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._image_display)

        self._tab_name_enum = tab_name_enum


    def get_image_display(self) -> ImageDisplay:
        return self._image_display


    def get_tab_name_enum(self) -> TabName:
        return self._tab_name_enum
