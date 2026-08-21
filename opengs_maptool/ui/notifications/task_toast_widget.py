import traceback
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, QEvent
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QVBoxLayout, QGraphicsOpacityEffect, QWidget
)
from opengs_maptool.models.progress_status import ProgressStatus
from opengs_maptool.ui.modals.error_modal import ErrorModal


class TaskToastWidget(QFrame):
    def __init__(self, title: str, main_window: QWidget | None = None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setObjectName("taskToast")
        self._title = title
        self._main_window = main_window
        self._last_error: BaseException | None = None
        self._theme = {}
        self._is_dark_theme: bool | None = None
        self._applying_theme = False

        self._apply_theme()

        # Set up opacity effect for smooth fade-outs
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)

        # Layout setup
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")

        self.status_label = QLabel("Starting...")
        self.status_label.setObjectName("statusLabel")

        self.close_btn = QPushButton("x")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(22, 22)
        self.close_btn.clicked.connect(self._on_close_clicked)
        self.close_btn.hide()

        top_row.addWidget(self.title_label)
        top_row.addStretch()
        top_row.addWidget(self.close_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)

        # Bottom row for error action buttons
        self.bottom_row = QHBoxLayout()
        self.bottom_row.setSpacing(8)
        self.details_btn = QPushButton("Show Details")
        self.details_btn.setObjectName("detailsBtn")
        self.details_btn.clicked.connect(self.show_error_modal)
        self.details_btn.hide()

        self.bottom_row.addWidget(self.status_label)
        self.bottom_row.addStretch()
        self.bottom_row.addWidget(self.details_btn)

        layout.addLayout(top_row)
        layout.addLayout(self.bottom_row)
        layout.addWidget(self.progress_bar)

        # Internal state
        self._task_signals = None
        self._is_active = False
        self._current_phase_description = "Working"
        self._set_status_tone("muted", bold=False)

    def _is_dark_palette(self) -> bool:
        return self.palette().window().color().lightness() < 128

    def _build_theme(self, is_dark: bool) -> dict[str, str]:
        # Use the window brush directly for compatibility across PyQt6 builds.
        if is_dark:
            return {
                "bg_top": "#2c3858",
                "bg_bottom": "#24304d",
                "border": "#5168a0",
                "text": "#f6f8ff",
                "muted": "#d6e3ff",
                "progress_bg": "#1f2a43",
                "progress_chunk_start": "#67e8f9",
                "progress_chunk_end": "#3b82f6",
                "close_fg": "#edf4ff",
                "close_hover": "#435987",
                "details_bg": "#ff8f3f",
                "details_hover": "#ff9d57",
                "success": "#7af0b0",
                "warning": "#ffd86b",
                "error": "#ff8e9e",
                "cancelled": "#cad7f5",
            }

        return {
            "bg_top": "#ffffff",
            "bg_bottom": "#eef8ff",
            "border": "#bdd8f3",
            "text": "#13253a",
            "muted": "#24527a",
            "progress_bg": "#d9edff",
            "progress_chunk_start": "#22d3ee",
            "progress_chunk_end": "#0a84ff",
            "close_fg": "#1f4467",
            "close_hover": "#d7ebff",
            "details_bg": "#ff8a3d",
            "details_hover": "#ff9a56",
            "success": "#1b9154",
            "warning": "#a96800",
            "error": "#cc2f3e",
            "cancelled": "#36536f",
        }

    def _apply_theme(self, force: bool = False) -> None:
        if self._applying_theme:
            return

        is_dark = self._is_dark_palette()
        if not force and self._is_dark_theme == is_dark:
            return

        self._applying_theme = True
        self._is_dark_theme = is_dark
        self._theme = self._build_theme(is_dark)
        t = self._theme
        try:
            self.setStyleSheet(
                f"""
                QFrame#taskToast {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {t['bg_top']}, stop:1 {t['bg_bottom']});
                    border-radius: 10px;
                    border: 1px solid {t['border']};
                }}
                QLabel {{
                    color: {t['text']};
                    font-size: 11px;
                }}
                QLabel#titleLabel {{
                    font-weight: 700;
                    font-size: 12px;
                    color: {t['text']};
                }}
                QLabel#statusLabel {{
                    color: {t['muted']};
                }}
                QProgressBar {{
                    border: 1px solid {t['border']};
                    border-radius: 4px;
                    background: {t['progress_bg']};
                }}
                QProgressBar::chunk {{
                    border-radius: 3px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {t['progress_chunk_start']}, stop:1 {t['progress_chunk_end']});
                }}
                QPushButton#closeBtn {{
                    border: none;
                    border-radius: 11px;
                    color: {t['close_fg']};
                    font-size: 12px;
                    font-weight: 700;
                    background: transparent;
                }}
                QPushButton#closeBtn:hover {{
                    background: {t['close_hover']};
                }}
                QPushButton#closeBtn:disabled {{
                    color: {t['muted']};
                }}
                QPushButton#detailsBtn {{
                    border: none;
                    border-radius: 4px;
                    padding: 3px 9px;
                    font-size: 10px;
                    font-weight: 700;
                    color: #ffffff;
                    background: {t['details_bg']};
                }}
                QPushButton#detailsBtn:hover {{
                    background: {t['details_hover']};
                }}
                """
            )
        finally:
            self._applying_theme = False

    def _set_status_tone(self, tone: str, *, bold: bool = True) -> None:
        color = self._theme.get(tone, self._theme["muted"])
        weight = "700" if bold else "500"
        self.status_label.setStyleSheet(f"color: {color}; font-weight: {weight};")

    def changeEvent(self, event: QEvent) -> None:
        super().changeEvent(event)
        if event.type() in (QEvent.Type.PaletteChange, QEvent.Type.ApplicationPaletteChange):
            self._apply_theme()

    def show_error_modal(self) -> None:
        """Opens the modal dialog detailing the exception that occurred."""
        if self._last_error is None:
            return

        error_text = (
            f"Task '{self._title}' failed with error:\n"
            f"{str(self._last_error)}\n\n"
            + "".join(traceback.format_exception(self._last_error))
        )
        error_modal = ErrorModal(
            main_window=self._main_window,
            error_text=error_text
        )
        error_modal.exec()

    def on_phase_started(self, phase_description: str, status: ProgressStatus) -> None:
        self._current_phase_description = phase_description or "Working"

        # Keep progress visuals in sync when a phase starts before the next update tick.
        self.progress_bar.setRange(0, status.total_steps)
        self.progress_bar.setValue(status.completed_steps)

        if status.total_steps > 0:
            pct = int((status.completed_steps / status.total_steps) * 100)
            self.status_label.setText(f"{self._current_phase_description}... {pct}%")
        else:
            self.status_label.setText(f"{self._current_phase_description}...")
        self._set_status_tone("muted", bold=False)

    def on_progress_started(self, status: ProgressStatus) -> None:
        self.progress_bar.setRange(0, status.total_steps)
        self.progress_bar.setValue(status.completed_steps)
        self.status_label.setText(f"{self._current_phase_description}...")
        self._set_status_tone("muted", bold=False)
        self._is_active = True
        self.close_btn.show()

    def on_progress_updated(self, status: ProgressStatus, steps_increased: int) -> None:
        self.progress_bar.setRange(0, status.total_steps)
        self.progress_bar.setValue(status.completed_steps)

        if status.total_steps > 0:
            pct = int((status.completed_steps / status.total_steps) * 100)
            self.status_label.setText(f"{self._current_phase_description}... {pct}%")
            self._set_status_tone("muted", bold=False)

    def fade_out_and_close(self, duration_ms: int = 400) -> None:
        """Smoothly fades out the toast widget before removing it."""
        self.anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self.anim.setDuration(duration_ms)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.finished.connect(self.close)
        self.anim.start()

    def set_task_signals(self, signals) -> None:
        """Give the toast access to the task's signals so it can request cancellation."""
        self._task_signals = signals

    def on_success(self, result: object) -> None:
        self.progress_bar.setValue(self.progress_bar.maximum())
        self.status_label.setText("Completed")
        self._set_status_tone("success")
        self._is_active = False
        self.close_btn.show()

        QTimer.singleShot(2500, self.fade_out_and_close)

    def on_error(self, error: BaseException) -> None:
        self._last_error = error
        self.progress_bar.hide()
        self.status_label.setText(f"Failed: {str(error)}")
        self._set_status_tone("error")
        self.details_btn.show()
        self._is_active = False
        self.close_btn.show()

        # Automatically pop open the modal on error arrival
        self.show_error_modal()
        traceback.print_exception(type(error), error, error.__traceback__)

    def on_retired(self) -> None:
        """Called when the ProgressController is retired (owner requested cancel or normal retire)."""
        if self._is_active:
            # Owner requested cancel — show cancelling state immediately
            self.status_label.setText("Cancelling...")
            self._set_status_tone("warning")
            # Keep the cancel button visible but disabled to indicate request sent
            self.close_btn.setEnabled(False)

    def _on_close_clicked(self) -> None:
        """Handle clicks on the top-right 'x'. Acts as cancel when active, otherwise closes."""
        if self._is_active:
            # Request cancellation via task signals if available
            if self._task_signals is not None:
                self._task_signals.task_cancel_requested.emit()
            # Update UI immediately
            self.status_label.setText("Cancelling...")
            self._set_status_tone("warning")
            self.close_btn.setEnabled(False)
        else:
            self.fade_out_and_close()

    def on_cancelled(self) -> None:
        """Called when the worker thread reports it has exited due to cancellation."""
        self.progress_bar.hide()
        self.status_label.setText("Cancelled")
        self._set_status_tone("cancelled")
        QTimer.singleShot(1200, self.fade_out_and_close)
