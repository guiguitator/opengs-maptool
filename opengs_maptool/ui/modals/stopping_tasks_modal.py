from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QDialogButtonBox,
    QPushButton,
    QWidget,
)

from opengs_maptool.controllers.task_controller import TaskController


class StoppingTasksModal(QDialog):
    """
    Modal dialog shown while background tasks are being stopped.
    Requests cancellation of all running tasks and waits for them to finish.
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Stopping background tasks")
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setMinimumSize(420, 120)

        self._label = QLabel("Stopping background tasks before closing automatically. This may take a moment...")
        self._label.setWordWrap(True)

        self._progress = QProgressBar()
        # Indeterminate busy indicator
        self._progress.setRange(0, 0)
        self._progress.setTextVisible(False)

        self._button_box = QDialogButtonBox()
        self._force_btn = QPushButton("Force Quit (dangerous)")
        self._force_btn.setEnabled(False)
        self._force_btn.clicked.connect(self._on_force)
        self._button_box.addButton(self._force_btn, QDialogButtonBox.ButtonRole.ActionRole)

        layout = QVBoxLayout(self)
        layout.addWidget(self._label)
        layout.addWidget(self._progress)
        layout.addWidget(self._button_box)

        self._task_controller: TaskController | None = None
        self._result: bool | None = None

        self._apply_theme()

    def _apply_theme(self) -> None:
        # Adapt to dark or light system palette for a subtle look
        pal = self.palette()
        window_color = pal.color(QPalette.ColorRole.Window)
        # Lightness ranges 0 (black) .. 255 (white)
        lightness = window_color.lightness()
        if lightness < 128:
            # dark theme: brighten text
            self.setStyleSheet("QDialog { background: #2b2b2b; color: #ffffff; }")
            self._label.setStyleSheet("color: #e0e0e0")
        else:
            self.setStyleSheet("QDialog { background: #ffffff; color: #111111; }")
            self._label.setStyleSheet("color: #222222")

    def start_and_wait(self, task_controller: TaskController, timeout_ms: int | None = None) -> bool:
        """
        Show the modal, request cancellation of running tasks and wait.

        This method returns True if all tasks terminated before timeout, False otherwise.
        """
        self._task_controller = task_controller

        # Defer the actual cancel/start to allow the dialog to render first
        QTimer.singleShot(0, lambda: self._begin_cancel(max_wait_ms=timeout_ms))

        # Run the dialog (nested event loop) until _begin_cancel closes it
        self.exec()

        return bool(self._result)

    def _begin_cancel(self, max_wait_ms: int | None) -> None:
        if self._task_controller is None:
            self._result = True
            self.accept()
            return

        # Only show the dialog if there are running tasks
        # If there are none, cancel_all_and_wait will return True immediately
        success = self._task_controller.cancel_all_and_wait(max_wait_ms=max_wait_ms)

        if success:
            self._result = True
            self.accept()
        else:
            # Timed out — enable force option and update text
            self._result = False
            self._label.setText("Timed out while stopping background tasks. You can force quit, but unsaved work may be lost.")
            self._force_btn.setEnabled(True)

    def _on_force(self) -> None:
        # Close dialog and indicate force; caller can decide next steps
        self._result = False
        self.accept()
