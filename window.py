"""
ui/window.py
============
Anarchy Cyberpunk — Minecraft Instance Lifecycle Manager & Automation Dashboard
Ultra-premium PyQt5 desktop UI for Bazzite/Fedora Silverblue immutable environments.

Author  : Principal Python / PyQt5 Architect
Theme   : High-contrast dark luxury — "Anarchy Cyberpunk"
Requires: PyQt5 >= 5.15, requests, pyperclip (optional)
"""

from __future__ import annotations

import os
import subprocess
import sys
import uuid
from datetime import datetime
from typing import Optional

from PyQt5.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QThread,
    QTimer,
    pyqtSignal,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontDatabase,
    QIcon,
    QPainter,
    QPalette,
    QPen,
    QPixmap,
    QTextCharFormat,
    QTextCursor,
)
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL DESIGN TOKENS
# ─────────────────────────────────────────────────────────────────────────────

C_BG          = "#0A0A0C"        # Primary window canvas
C_CARD        = "#141419"        # Interactive component blocks / cards
C_CARD_HOVER  = "#1C1C24"        # Slightly lighter card on hover
C_BORDER      = "#2A2A35"        # Subtle border / separator
C_VIOLET      = "#8A2BE2"        # Primary action / brand accent (Electric Neon Violet)
C_VIOLET_DIM  = "#5A1BAF"        # Dimmed violet for gradients / shadows
C_CYAN        = "#00FFFF"        # Secondary interactive states (Cyber Cyan)
C_LIME        = "#39FF14"        # Success / verification (Neon Lime)
C_CRIMSON     = "#FF3131"        # System terminal / error (Neon Crimson)
C_GOLD        = "#FFD700"        # Warning state (Gold)
C_TEXT        = "#E8E8F0"        # Primary readable text
C_TEXT_DIM    = "#7A7A9A"        # Secondary / muted text
C_SIDEBAR_W   = 220              # Sidebar pixel width


# ─────────────────────────────────────────────────────────────────────────────
# STYLESHEET — Single source of truth for the entire application skin
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_QSS = f"""
/* ── Root & Window ───────────────────────────────────────────────────────── */
QMainWindow, QDialog, QWidget {{
    background-color: {C_BG};
    color: {C_TEXT};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
}}

/* ── Scroll Bars ─────────────────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: {C_CARD};
    width: 7px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {C_VIOLET};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {C_CARD};
    height: 7px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {C_VIOLET};
    border-radius: 3px;
    min-width: 24px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ── General Push Button ─────────────────────────────────────────────────── */
QPushButton {{
    background-color: {C_CARD};
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 7px 18px;
    font-family: "Consolas", monospace;
    font-size: 12px;
    font-weight: bold;
}}
QPushButton:hover {{
    border-color: {C_VIOLET};
    color: {C_VIOLET};
    background-color: {C_CARD_HOVER};
}}
QPushButton:pressed {{
    background-color: {C_VIOLET_DIM};
    color: #FFFFFF;
}}
QPushButton:disabled {{
    color: {C_TEXT_DIM};
    border-color: {C_BORDER};
}}

/* ── Accent Buttons (primary CTA) ───────────────────────────────────────── */
QPushButton#accentBtn {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {C_VIOLET_DIM}, stop:1 {C_VIOLET});
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 22px;
    font-size: 13px;
}}
QPushButton#accentBtn:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {C_VIOLET}, stop:1 {C_CYAN});
    color: #000000;
}}

/* ── Danger Buttons ──────────────────────────────────────────────────────── */
QPushButton#dangerBtn {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #8B0000, stop:1 {C_CRIMSON});
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 22px;
    font-weight: bold;
}}
QPushButton#dangerBtn:hover {{
    background: {C_CRIMSON};
    color: #000;
}}

/* ── Success Buttons ─────────────────────────────────────────────────────── */
QPushButton#successBtn {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #1A6600, stop:1 {C_LIME});
    color: #000000;
    border: none;
    border-radius: 6px;
    padding: 8px 22px;
    font-weight: bold;
}}
QPushButton#successBtn:hover {{ background: {C_LIME}; }}

/* ── Line Edits & Spin Boxes ─────────────────────────────────────────────── */
QLineEdit, QSpinBox {{
    background-color: {C_CARD};
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
    border-radius: 5px;
    padding: 6px 10px;
    selection-background-color: {C_VIOLET};
    font-family: "Consolas", monospace;
}}
QLineEdit:focus, QSpinBox:focus {{
    border-color: {C_VIOLET};
}}

/* ── Combo Box ───────────────────────────────────────────────────────────── */
QComboBox {{
    background-color: {C_CARD};
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
    border-radius: 5px;
    padding: 6px 10px;
    min-width: 120px;
}}
QComboBox:hover {{ border-color: {C_VIOLET}; }}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid {C_BORDER};
}}
QComboBox QAbstractItemView {{
    background-color: {C_CARD};
    color: {C_TEXT};
    border: 1px solid {C_VIOLET};
    selection-background-color: {C_VIOLET_DIM};
}}

/* ── Sliders ─────────────────────────────────────────────────────────────── */
QSlider::groove:horizontal {{
    border: none;
    height: 4px;
    background: {C_BORDER};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {C_VIOLET};
    border: none;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::handle:horizontal:hover {{ background: {C_CYAN}; }}
QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {C_VIOLET_DIM}, stop:1 {C_VIOLET});
    border-radius: 2px;
}}

/* ── Text Edit (terminal / logs) ─────────────────────────────────────────── */
QTextEdit {{
    background-color: #06060A;
    color: {C_CYAN};
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    selection-background-color: {C_VIOLET_DIM};
}}

/* ── List Widget ─────────────────────────────────────────────────────────── */
QListWidget {{
    background-color: {C_CARD};
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{ padding: 8px 12px; border-radius: 4px; }}
QListWidget::item:hover {{ background-color: {C_CARD_HOVER}; color: {C_CYAN}; }}
QListWidget::item:selected {{
    background-color: {C_VIOLET_DIM};
    color: #FFFFFF;
    border: none;
}}

/* ── Tab Widget ──────────────────────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    background: {C_CARD};
}}
QTabBar::tab {{
    background: {C_BG};
    color: {C_TEXT_DIM};
    padding: 8px 18px;
    border-bottom: 2px solid transparent;
    font-family: "Consolas", monospace;
    font-size: 12px;
}}
QTabBar::tab:selected {{
    color: {C_VIOLET};
    border-bottom: 2px solid {C_VIOLET};
    background: {C_CARD};
}}
QTabBar::tab:hover {{ color: {C_TEXT}; }}

/* ── Group Box ───────────────────────────────────────────────────────────── */
QGroupBox {{
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    margin-top: 14px;
    padding: 12px 8px 8px 8px;
    color: {C_TEXT_DIM};
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    color: {C_VIOLET};
    font-weight: bold;
}}

/* ── Progress Bar ────────────────────────────────────────────────────────── */
QProgressBar {{
    background-color: {C_CARD};
    border: 1px solid {C_BORDER};
    border-radius: 5px;
    height: 10px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {C_VIOLET_DIM}, stop:1 {C_VIOLET});
    border-radius: 5px;
}}

/* ── Checkbox ────────────────────────────────────────────────────────────── */
QCheckBox {{
    color: {C_TEXT};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 1px solid {C_BORDER};
    border-radius: 3px;
    background: {C_CARD};
}}
QCheckBox::indicator:checked {{
    background: {C_VIOLET};
    border-color: {C_VIOLET};
}}

/* ── Status Bar ──────────────────────────────────────────────────────────── */
QStatusBar {{
    background-color: {C_CARD};
    color: {C_TEXT_DIM};
    border-top: 1px solid {C_BORDER};
    font-size: 11px;
}}
"""


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def glow_effect(widget: QWidget, color: str = C_VIOLET, radius: int = 18) -> None:
    """Attach a subtle drop-shadow glow to any widget."""
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(radius)
    effect.setOffset(0, 0)
    effect.setColor(QColor(color))
    widget.setGraphicsEffect(effect)


def section_label(text: str, color: str = C_TEXT_DIM) -> QLabel:
    """Return a styled uppercase section-header label."""
    lbl = QLabel(text.upper())
    lbl.setStyleSheet(
        f"color: {color}; font-size: 10px; letter-spacing: 2px; "
        f"font-weight: bold; padding: 4px 0;"
    )
    return lbl


def divider() -> QFrame:
    """Return a thin horizontal divider rule."""
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"color: {C_BORDER}; background: {C_BORDER};")
    line.setFixedHeight(1)
    return line


def accent_button(text: str, icon_char: str = "") -> QPushButton:
    btn = QPushButton(f"{icon_char}  {text}" if icon_char else text)
    btn.setObjectName("accentBtn")
    return btn


def danger_button(text: str, icon_char: str = "") -> QPushButton:
    btn = QPushButton(f"{icon_char}  {text}" if icon_char else text)
    btn.setObjectName("dangerBtn")
    return btn


def success_button(text: str, icon_char: str = "") -> QPushButton:
    btn = QPushButton(f"{icon_char}  {text}" if icon_char else text)
    btn.setObjectName("successBtn")
    return btn


def card_widget(parent: Optional[QWidget] = None) -> QWidget:
    """Return a styled card-surface container widget."""
    w = QWidget(parent)
    w.setStyleSheet(
        f"background-color: {C_CARD}; border: 1px solid {C_BORDER}; "
        f"border-radius: 10px;"
    )
    return w


# ─────────────────────────────────────────────────────────────────────────────
# WORKER THREADS
# ─────────────────────────────────────────────────────────────────────────────

class DownloadWorker(QThread):
    """
    Generic asynchronous download/task worker.
    Emits progress (0-100), log messages, and a finished signal.
    """

    progress_signal = pyqtSignal(int)          # 0–100
    log_signal      = pyqtSignal(str, str)     # (message, level) level in [info|warn|error]
    finished_signal = pyqtSignal(bool, str)    # (success, message)

    def __init__(self, task_fn, *args, **kwargs):
        super().__init__()
        self._task_fn = task_fn
        self._args    = args
        self._kwargs  = kwargs

    def run(self) -> None:
        try:
            self._task_fn(self, *self._args, **self._kwargs)
            self.finished_signal.emit(True, "Task completed successfully.")
        except Exception as exc:
            self.log_signal.emit(f"Worker error: {exc}", "error")
            self.finished_signal.emit(False, str(exc))


class ProcessMonitorWorker(QThread):
    """
    Monitors a running subprocess, streaming stdout/stderr in real time.
    Attaches to the subprocess.Popen object supplied by the caller.
    """

    output_signal   = pyqtSignal(str, str)   # (line, level)
    finished_signal = pyqtSignal(int)         # exit code

    def __init__(self, proc: subprocess.Popen):
        super().__init__()
        self._proc = proc

    def run(self) -> None:
        try:
            for raw_line in iter(self._proc.stdout.readline, b""):
                line = raw_line.decode("utf-8", errors="replace").rstrip()
                if not line:
                    continue
                level = "info"
                lo = line.lower()
                if "warn" in lo:
                    level = "warn"
                elif any(k in lo for k in ("error", "exception", "fatal", "crash")):
                    level = "error"
                self.output_signal.emit(line, level)
            self._proc.wait()
            self.finished_signal.emit(self._proc.returncode)
        except Exception as exc:
            self.output_signal.emit(f"[Monitor error] {exc}", "error")
            self.finished_signal.emit(-1)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

class NavButton(QPushButton):
    """
    Left-sidebar navigation pill button.
    Highlights the active panel with a violet left-border accent line.
    """

    def __init__(self, icon: str, label: str, parent=None):
        super().__init__(parent)
        self._icon  = icon
        self._label = label
        self._active = False
        self.setText(f"  {icon}   {label}")
        self.setFixedHeight(46)
        self.setCursor(Qt.PointingHandCursor)
        self._apply_style()

    def set_active(self, active: bool) -> None:
        self._active = active
        self._apply_style()

    def _apply_style(self) -> None:
        if self._active:
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background-color: {C_CARD_HOVER};"
                f"  color: {C_VIOLET};"
                f"  border: none;"
                f"  border-left: 3px solid {C_VIOLET};"
                f"  border-radius: 0px;"
                f"  text-align: left;"
                f"  padding-left: 14px;"
                f"  font-weight: bold;"
                f"  font-size: 13px;"
                f"  font-family: Consolas, monospace;"
                f"}}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background-color: transparent;"
                f"  color: {C_TEXT_DIM};"
                f"  border: none;"
                f"  border-left: 3px solid transparent;"
                f"  border-radius: 0px;"
                f"  text-align: left;"
                f"  padding-left: 14px;"
                f"  font-size: 13px;"
                f"  font-family: Consolas, monospace;"
                f"}}"
                f"QPushButton:hover {{"
                f"  background-color: {C_CARD};"
                f"  color: {C_TEXT};"
                f"}}"
            )


class SidebarWidget(QWidget):
    """
    Left navigation command deck.
    Emits `nav_changed(index)` when the user selects a new panel.
    """

    nav_changed = pyqtSignal(int)

    _NAV_ITEMS = [
        ("⬡", "Instance Matrix"),
        ("◈", "Add-on Repository"),
        ("◉", "Identity Center"),
        ("◫", "System Tuning"),
        ("◬", "Engine Telemetry"),
        ("◐", "AI Bot Deck"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(C_SIDEBAR_W)
        self.setStyleSheet(
            f"background-color: {C_CARD}; border-right: 1px solid {C_BORDER};"
        )
        self._buttons: list[NavButton] = []
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Logo / brand strip ────────────────────────────────────────────
        brand = QWidget()
        brand.setFixedHeight(64)
        brand.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {C_VIOLET_DIM},stop:1 #0A0A0C);"
            f"border-bottom: 1px solid {C_BORDER};"
        )
        bl = QVBoxLayout(brand)
        bl.setContentsMargins(16, 0, 0, 0)
        title_lbl = QLabel("⚡ NETHER CORE")
        title_lbl.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 15px; font-weight: bold; "
            f"font-family: Consolas, monospace; letter-spacing: 2px; "
            f"background: transparent; border: none;"
        )
        sub_lbl = QLabel("Instance Manager v2.0")
        sub_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 10px; "
            f"background: transparent; border: none;"
        )
        bl.addWidget(title_lbl)
        bl.addWidget(sub_lbl)
        layout.addWidget(brand)

        # ── Navigation pills ──────────────────────────────────────────────
        layout.addSpacing(12)
        layout.addWidget(section_label("  Navigation"))
        layout.addSpacing(4)

        for idx, (icon, label) in enumerate(self._NAV_ITEMS):
            btn = NavButton(icon, label)
            btn.clicked.connect(lambda checked, i=idx: self._on_nav(i))
            self._buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()
        layout.addWidget(divider())

        # ── Status strip ──────────────────────────────────────────────────
        self._status_strip = QLabel("◉ IDLE")
        self._status_strip.setStyleSheet(
            f"color: {C_LIME}; font-size: 11px; padding: 8px 16px; "
            f"background: transparent; border: none;"
        )
        layout.addWidget(self._status_strip)

        self._buttons[0].set_active(True)

    def _on_nav(self, index: int) -> None:
        for i, btn in enumerate(self._buttons):
            btn.set_active(i == index)
        self.nav_changed.emit(index)

    def set_status(self, text: str, color: str = C_LIME) -> None:
        self._status_strip.setText(text)
        self._status_strip.setStyleSheet(
            f"color: {color}; font-size: 11px; padding: 8px 16px; "
            f"background: transparent; border: none;"
        )


# ─────────────────────────────────────────────────────────────────────────────
# PANEL 1 — INSTANCE MATRIX & MODPACK HUB
# ─────────────────────────────────────────────────────────────────────────────

class InstanceCard(QWidget):
    """
    Visual card representing one Minecraft installation instance.
    Shows version, loader, last-launch time, and action buttons.
    """

    launch_requested = pyqtSignal(dict)
    clone_requested  = pyqtSignal(dict)
    delete_requested = pyqtSignal(dict)

    def __init__(self, instance_data: dict, parent=None):
        super().__init__(parent)
        self._data = instance_data
        self.setFixedSize(220, 160)
        self._build_ui()
        glow_effect(self, C_VIOLET, 10)

    def _build_ui(self) -> None:
        self.setStyleSheet(
            f"background-color: {C_CARD}; border: 1px solid {C_BORDER}; "
            f"border-radius: 10px;"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # ── Header row ────────────────────────────────────────────────────
        header = QHBoxLayout()
        icon_lbl = QLabel(self._data.get("icon", "⬡"))
        icon_lbl.setStyleSheet(
            f"font-size: 22px; color: {C_VIOLET}; background: transparent; border: none;"
        )
        name_lbl = QLabel(self._data.get("name", "Unnamed"))
        name_lbl.setStyleSheet(
            f"color: {C_TEXT}; font-weight: bold; font-size: 13px; "
            f"background: transparent; border: none;"
        )
        header.addWidget(icon_lbl)
        header.addWidget(name_lbl)
        header.addStretch()
        layout.addLayout(header)

        # ── Version / loader badges ───────────────────────────────────────
        badge_row = QHBoxLayout()
        badge_row.setSpacing(6)
        ver_badge = self._badge(self._data.get("version", "?"), C_CYAN)
        loader_badge = self._badge(self._data.get("loader", "Vanilla"), C_VIOLET)
        badge_row.addWidget(ver_badge)
        badge_row.addWidget(loader_badge)
        badge_row.addStretch()
        layout.addLayout(badge_row)

        # ── Last launch ───────────────────────────────────────────────────
        last_lbl = QLabel(f"Last: {self._data.get('last_launch', 'Never')}")
        last_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 10px; background: transparent; border: none;"
        )
        layout.addWidget(last_lbl)

        layout.addStretch()

        # ── Action buttons ────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        launch_btn = QPushButton("▶")
        launch_btn.setFixedSize(32, 28)
        launch_btn.setToolTip("Launch Instance")
        launch_btn.setStyleSheet(
            f"background: {C_VIOLET_DIM}; color: #FFF; border: none; border-radius: 5px; "
            f"font-size: 13px;"
        )
        launch_btn.clicked.connect(lambda: self.launch_requested.emit(self._data))

        clone_btn = QPushButton("⎘")
        clone_btn.setFixedSize(32, 28)
        clone_btn.setToolTip("Clone Instance")
        clone_btn.setStyleSheet(
            f"background: {C_CARD_HOVER}; color: {C_CYAN}; border: 1px solid {C_BORDER}; "
            f"border-radius: 5px; font-size: 13px;"
        )
        clone_btn.clicked.connect(lambda: self.clone_requested.emit(self._data))

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(32, 28)
        del_btn.setToolTip("Delete Instance")
        del_btn.setStyleSheet(
            f"background: #1A0000; color: {C_CRIMSON}; border: 1px solid #3A0000; "
            f"border-radius: 5px; font-size: 13px;"
        )
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self._data))

        btn_row.addWidget(launch_btn)
        btn_row.addWidget(clone_btn)
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    @staticmethod
    def _badge(text: str, color: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"background-color: {color}22; color: {color}; border: 1px solid {color}55; "
            f"border-radius: 4px; padding: 1px 7px; font-size: 10px; font-weight: bold;"
        )
        return lbl


class InstanceMatrixPanel(QWidget):
    """
    Panel 1 — Manages the grid of instance cards, modpack ingestion,
    and instance cloning / export workflows.
    """

    # Forwarded from cards to the main window telemetry
    launch_requested = pyqtSignal(dict)

    # Minimal mock dataset; in production this would deserialise from ~/.local/share/nethercore/
    _DEFAULT_INSTANCES: list[dict] = [
        {
            "id": str(uuid.uuid4()),
            "icon": "⬡",
            "name": "Survival Hardcore",
            "version": "1.21.1",
            "loader": "Fabric",
            "last_launch": "2025-08-10 14:33",
        },
        {
            "id": str(uuid.uuid4()),
            "icon": "◈",
            "name": "Create Automation",
            "version": "1.20.1",
            "loader": "Forge",
            "last_launch": "2025-08-09 09:11",
        },
        {
            "id": str(uuid.uuid4()),
            "icon": "◉",
            "name": "Dev Sandbox",
            "version": "1.21",
            "loader": "NeoForge",
            "last_launch": "Never",
        },
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._instances: list[dict] = list(self._DEFAULT_INSTANCES)
        self._cards: list[InstanceCard] = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # ── Header ────────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        title = QLabel("⬡  Instance Matrix")
        title.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 18px; font-weight: bold; "
            f"font-family: Consolas, monospace;"
        )
        new_btn = accent_button("+ New Instance", "⬡")
        new_btn.clicked.connect(self._create_new_instance)
        import_btn = QPushButton("⬆  Import ZIP")
        import_btn.clicked.connect(self._import_zip)
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(import_btn)
        hdr.addWidget(new_btn)
        root.addLayout(hdr)
        root.addWidget(divider())

        # ── Instance card grid ────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        self._grid_container = QWidget()
        self._grid_container.setStyleSheet("background: transparent;")
        self._grid_layout = QGridLayout(self._grid_container)
        self._grid_layout.setSpacing(16)
        self._grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        scroll.setWidget(self._grid_container)
        root.addWidget(scroll, stretch=3)

        self._refresh_grid()

        # ── Modpack ingestion section ─────────────────────────────────────
        root.addWidget(divider())
        root.addWidget(section_label("Modpack Ingest Engine", C_CYAN))

        ingest_card = card_widget()
        ingest_layout = QVBoxLayout(ingest_card)
        ingest_layout.setContentsMargins(16, 14, 16, 14)
        ingest_layout.setSpacing(10)

        src_row = QHBoxLayout()
        self._pack_source_combo = QComboBox()
        self._pack_source_combo.addItems(["Modrinth", "CurseForge", "FTB", "Technic"])
        self._pack_url_edit = QLineEdit()
        self._pack_url_edit.setPlaceholderText("Paste modpack URL or manifest slug…")
        ingest_btn = accent_button("Ingest Modpack")
        ingest_btn.clicked.connect(self._ingest_modpack)
        src_row.addWidget(self._pack_source_combo)
        src_row.addWidget(self._pack_url_edit, stretch=1)
        src_row.addWidget(ingest_btn)
        ingest_layout.addLayout(src_row)

        self._ingest_progress = QProgressBar()
        self._ingest_progress.setVisible(False)
        self._ingest_progress.setFixedHeight(10)
        ingest_layout.addWidget(self._ingest_progress)

        self._ingest_status = QLabel("")
        self._ingest_status.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 11px;"
        )
        ingest_layout.addWidget(self._ingest_status)
        root.addWidget(ingest_card)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _refresh_grid(self) -> None:
        """Rebuild the instance card grid from the current instances list."""
        # Clear previous cards
        for i in reversed(range(self._grid_layout.count())):
            widget = self._grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self._cards.clear()

        cols = 4
        for idx, inst in enumerate(self._instances):
            card = InstanceCard(inst)
            card.launch_requested.connect(self._on_launch)
            card.clone_requested.connect(self._on_clone)
            card.delete_requested.connect(self._on_delete)
            self._cards.append(card)
            self._grid_layout.addWidget(card, idx // cols, idx % cols)

    def _create_new_instance(self) -> None:
        """Open a simple dialog to create a new instance entry."""
        dlg = NewInstanceDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self._instances.append(dlg.get_instance_data())
            self._refresh_grid()

    def _import_zip(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Instance ZIP", os.path.expanduser("~"),
            "ZIP Archives (*.zip)"
        )
        if path:
            QMessageBox.information(
                self, "Import",
                f"Instance ZIP queued for extraction:\n{path}\n\n"
                "(Full extraction pipeline would run here in production.)"
            )

    def _ingest_modpack(self) -> None:
        url = self._pack_url_edit.text().strip()
        source = self._pack_source_combo.currentText()
        if not url:
            self._ingest_status.setText("⚠  Please enter a modpack URL or slug first.")
            self._ingest_status.setStyleSheet(f"color: {C_GOLD};")
            return

        self._ingest_progress.setVisible(True)
        self._ingest_progress.setValue(0)
        self._ingest_status.setText(f"Connecting to {source} API…")
        self._ingest_status.setStyleSheet(f"color: {C_CYAN};")

        # Simulated progress ticker (replace with real DownloadWorker in production)
        self._ingest_timer = QTimer(self)
        self._ingest_timer.timeout.connect(self._tick_ingest)
        self._ingest_timer.start(120)

    def _tick_ingest(self) -> None:
        val = self._ingest_progress.value() + 5
        self._ingest_progress.setValue(val)
        if val >= 100:
            self._ingest_timer.stop()
            self._ingest_status.setText("✓  Modpack ingested successfully — new instance created.")
            self._ingest_status.setStyleSheet(f"color: {C_LIME};")
            self._pack_url_edit.clear()
            # Append a mock instance to the grid
            self._instances.append({
                "id": str(uuid.uuid4()),
                "icon": "◫",
                "name": "Ingested Pack",
                "version": "1.20.4",
                "loader": "Fabric",
                "last_launch": "Never",
            })
            self._refresh_grid()

    def _on_launch(self, data: dict) -> None:
        data["last_launch"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._refresh_grid()
        self.launch_requested.emit(data)

    def _on_clone(self, data: dict) -> None:
        clone = dict(data)
        clone["id"]   = str(uuid.uuid4())
        clone["name"] = data["name"] + " (Clone)"
        self._instances.append(clone)
        self._refresh_grid()

    def _on_delete(self, data: dict) -> None:
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Permanently delete instance '{data['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._instances = [i for i in self._instances if i["id"] != data["id"]]
            self._refresh_grid()


class NewInstanceDialog(QDialog):
    """Minimal dialog for creating a new Minecraft instance."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Instance")
        self.setFixedSize(420, 260)
        self.setStyleSheet(f"background: {C_BG}; color: {C_TEXT};")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        layout.addWidget(section_label("Create New Instance", C_VIOLET))

        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(14)

        self._name_edit    = QLineEdit(); self._name_edit.setPlaceholderText("Instance name…")
        self._version_edit = QLineEdit(); self._version_edit.setPlaceholderText("e.g. 1.21.1")
        self._loader_combo = QComboBox()
        self._loader_combo.addItems(["Vanilla", "Fabric", "Forge", "NeoForge", "Quilt"])
        self._icon_edit    = QLineEdit(); self._icon_edit.setPlaceholderText("Emoji icon e.g. ⬡")

        form_layout.addWidget(QLabel("Name"),    0, 0); form_layout.addWidget(self._name_edit, 0, 1)
        form_layout.addWidget(QLabel("Version"), 1, 0); form_layout.addWidget(self._version_edit, 1, 1)
        form_layout.addWidget(QLabel("Loader"),  2, 0); form_layout.addWidget(self._loader_combo, 2, 1)
        form_layout.addWidget(QLabel("Icon"),    3, 0); form_layout.addWidget(self._icon_edit, 3, 1)
        layout.addLayout(form_layout)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_instance_data(self) -> dict:
        return {
            "id":           str(uuid.uuid4()),
            "icon":         self._icon_edit.text() or "⬡",
            "name":         self._name_edit.text() or "New Instance",
            "version":      self._version_edit.text() or "1.21.1",
            "loader":       self._loader_combo.currentText(),
            "last_launch":  "Never",
        }


# ─────────────────────────────────────────────────────────────────────────────
# PANEL 2 — IN-LAUNCHER ADD-ON REPOSITORY & DEPENDENCY SOLVER
# ─────────────────────────────────────────────────────────────────────────────

class AddonRepositoryPanel(QWidget):
    """
    Panel 2 — Multi-source mod/shader/resource-pack browser
    with a visual dependency resolver alert area.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        # Header
        title = QLabel("◈  Add-on Repository")
        title.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 18px; font-weight: bold; font-family: Consolas;"
        )
        root.addWidget(title)
        root.addWidget(divider())

        # ── Search bar ────────────────────────────────────────────────────
        search_row = QHBoxLayout()
        self._source_combo = QComboBox()
        self._source_combo.addItems(["Modrinth", "CurseForge"])
        self._source_combo.setFixedWidth(130)
        self._type_combo = QComboBox()
        self._type_combo.addItems(["Mods", "Resource Packs", "Shaders", "Data Packs"])
        self._type_combo.setFixedWidth(140)
        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("Search mods, shaders, resource packs…")
        self._search_edit.returnPressed.connect(self._do_search)
        search_btn = accent_button("Search")
        search_btn.clicked.connect(self._do_search)
        search_row.addWidget(self._source_combo)
        search_row.addWidget(self._type_combo)
        search_row.addWidget(self._search_edit, stretch=1)
        search_row.addWidget(search_btn)
        root.addLayout(search_row)

        # ── Results list ──────────────────────────────────────────────────
        root.addWidget(section_label("Search Results", C_TEXT_DIM))
        self._result_list = QListWidget()
        self._result_list.setAlternatingRowColors(False)
        root.addWidget(self._result_list, stretch=2)

        install_btn = accent_button("⬇  Install Selected")
        install_btn.clicked.connect(self._install_selected)
        root.addWidget(install_btn)

        root.addWidget(divider())

        # ── Dependency resolver ───────────────────────────────────────────
        root.addWidget(section_label("Dependency Auto-Resolver", C_GOLD))

        dep_card = card_widget()
        dep_layout = QVBoxLayout(dep_card)
        dep_layout.setContentsMargins(14, 12, 14, 12)
        dep_layout.setSpacing(8)

        self._dep_alert = QLabel(
            "⚠  No pending dependency conflicts detected."
        )
        self._dep_alert.setWordWrap(True)
        self._dep_alert.setStyleSheet(
            f"color: {C_GOLD}; font-size: 12px; background: transparent;"
        )
        dep_layout.addWidget(self._dep_alert)

        self._dep_list = QListWidget()
        self._dep_list.setFixedHeight(80)
        dep_layout.addWidget(self._dep_list)

        resolve_btn = success_button("✓  Auto-Resolve & Download All")
        resolve_btn.clicked.connect(self._auto_resolve)
        dep_layout.addWidget(resolve_btn)

        root.addWidget(dep_card)
        root.addStretch()

        # Load mock results immediately
        self._populate_mock_results()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _populate_mock_results(self) -> None:
        """Seed the results list with representative mock data."""
        mock = [
            ("Fabric API",          "0.100.0+1.21",  "Modrinth",    "Required base API"),
            ("Sodium",              "0.5.11",        "Modrinth",    "Rendering optimiser"),
            ("Create",              "6.0.0-alpha",   "Modrinth",    "Automation machines"),
            ("Iris Shaders",        "1.7.5",         "Modrinth",    "Shader loader"),
            ("Continuity",          "3.0.0-beta.5",  "Modrinth",    "Connected textures"),
            ("JEI",                 "19.10.0.14",    "CurseForge",  "Item browser"),
            ("Complementary Shaders","r5.3",         "CurseForge",  "Ultra-quality shader"),
        ]
        for name, ver, source, desc in mock:
            item = QListWidgetItem(f"  {name}  ›  v{ver}  [{source}]  —  {desc}")
            item.setForeground(QColor(C_TEXT))
            self._result_list.addItem(item)

    def _do_search(self) -> None:
        query = self._search_edit.text().strip()
        if not query:
            return
        self._result_list.clear()
        # In production: dispatch DownloadWorker → API call → populate list
        item = QListWidgetItem(
            f"  (Simulated) Results for '{query}' on {self._source_combo.currentText()} — "
            f"[production: live API call]"
        )
        item.setForeground(QColor(C_CYAN))
        self._result_list.addItem(item)
        self._dep_alert.setText(
            f"⚠  Installing '{query}' may require: Fabric API ≥ 0.90.0, "
            f"Indium 1.0.34. Click Auto-Resolve to fetch automatically."
        )
        dep_items = ["▸ Fabric API 0.100.0+1.21", "▸ Indium 1.0.34"]
        self._dep_list.clear()
        for d in dep_items:
            di = QListWidgetItem(d)
            di.setForeground(QColor(C_GOLD))
            self._dep_list.addItem(di)

    def _install_selected(self) -> None:
        sel = self._result_list.selectedItems()
        if not sel:
            QMessageBox.warning(self, "No Selection", "Please select a mod to install.")
            return
        QMessageBox.information(
            self, "Install Queued",
            f"Queued for download:\n{sel[0].text()}\n\n"
            "(Full download pipeline would execute here.)"
        )

    def _auto_resolve(self) -> None:
        self._dep_list.clear()
        self._dep_alert.setText("✓  All dependencies resolved and queued for download.")
        self._dep_alert.setStyleSheet(f"color: {C_LIME}; font-size: 12px; background: transparent;")


# ─────────────────────────────────────────────────────────────────────────────
# PANEL 3 — IDENTITY CONTROL CENTER
# ─────────────────────────────────────────────────────────────────────────────

class IdentityCenterPanel(QWidget):
    """
    Panel 3 — Microsoft OAuth account management, offline personas,
    and active skin/cape preview area.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._accounts = [
            {"name": "Steve_Dev",    "type": "Microsoft",   "active": True},
            {"name": "LocalUser",    "type": "Offline",     "active": False},
            {"name": "TestRunner01", "type": "Offline",     "active": False},
        ]
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        title = QLabel("◉  Identity Control Center")
        title.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 18px; font-weight: bold; font-family: Consolas;"
        )
        root.addWidget(title)
        root.addWidget(divider())

        content_row = QHBoxLayout()
        content_row.setSpacing(20)

        # ── Account list ──────────────────────────────────────────────────
        left = QVBoxLayout()
        left.addWidget(section_label("Managed Profiles", C_TEXT_DIM))
        self._account_list = QListWidget()
        self._refresh_account_list()
        left.addWidget(self._account_list, stretch=1)

        acct_btn_row = QHBoxLayout()
        add_ms_btn = accent_button("+ Microsoft OAuth")
        add_ms_btn.clicked.connect(self._add_microsoft)
        add_offline_btn = QPushButton("+ Offline Persona")
        add_offline_btn.clicked.connect(self._add_offline)
        remove_btn = danger_button("✕ Remove")
        remove_btn.clicked.connect(self._remove_account)
        set_active_btn = success_button("✓ Set Active")
        set_active_btn.clicked.connect(self._set_active)
        acct_btn_row.addWidget(add_ms_btn)
        acct_btn_row.addWidget(add_offline_btn)
        acct_btn_row.addWidget(remove_btn)
        acct_btn_row.addWidget(set_active_btn)
        left.addLayout(acct_btn_row)
        content_row.addLayout(left, stretch=3)

        # ── Skin / cosmetic preview ───────────────────────────────────────
        right = QVBoxLayout()
        right.addWidget(section_label("Active Identity Preview", C_TEXT_DIM))

        skin_card = card_widget()
        skin_card.setFixedWidth(220)
        skin_layout = QVBoxLayout(skin_card)
        skin_layout.setContentsMargins(16, 16, 16, 16)
        skin_layout.setSpacing(10)
        skin_layout.setAlignment(Qt.AlignCenter)

        # ASCII art player silhouette
        player_art = QLabel(
            "     ██████     \n"
            "     ██████     \n"
            "   ██████████   \n"
            "   ██  ██  ██   \n"
            "   ██  ██  ██   \n"
            "   ██████████   \n"
            "     ██  ██     \n"
            "     ██  ██     \n"
        )
        player_art.setStyleSheet(
            f"color: {C_VIOLET}; font-family: Consolas, monospace; font-size: 11px; "
            f"background: transparent; letter-spacing: 0px;"
        )
        player_art.setAlignment(Qt.AlignCenter)
        skin_layout.addWidget(player_art)

        self._active_name_lbl = QLabel("Steve_Dev")
        self._active_name_lbl.setStyleSheet(
            f"color: {C_CYAN}; font-weight: bold; font-size: 14px; background: transparent;"
        )
        self._active_name_lbl.setAlignment(Qt.AlignCenter)
        skin_layout.addWidget(self._active_name_lbl)

        self._active_type_lbl = QLabel("Microsoft Account")
        self._active_type_lbl.setStyleSheet(
            f"color: {C_LIME}; font-size: 11px; background: transparent;"
        )
        self._active_type_lbl.setAlignment(Qt.AlignCenter)
        skin_layout.addWidget(self._active_type_lbl)

        skin_layout.addWidget(divider())

        cape_lbl = QLabel("Cape:  Anniversary Cape  ✓")
        cape_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 11px; background: transparent;"
        )
        cape_lbl.setAlignment(Qt.AlignCenter)
        skin_layout.addWidget(cape_lbl)

        upload_skin_btn = QPushButton("⬆  Upload Skin PNG")
        upload_skin_btn.clicked.connect(self._upload_skin)
        skin_layout.addWidget(upload_skin_btn)

        right.addWidget(skin_card)
        right.addStretch()
        content_row.addLayout(right, stretch=1)

        root.addLayout(content_row, stretch=1)
        root.addStretch()

    def _refresh_account_list(self) -> None:
        self._account_list.clear()
        for acc in self._accounts:
            star = "  ★ ACTIVE" if acc["active"] else ""
            item = QListWidgetItem(
                f"  {'●' if acc['type'] == 'Microsoft' else '○'}  "
                f"{acc['name']}  [{acc['type']}]{star}"
            )
            color = C_LIME if acc["active"] else C_TEXT
            item.setForeground(QColor(color))
            self._account_list.addItem(item)

    def _add_microsoft(self) -> None:
        QMessageBox.information(
            self, "Microsoft OAuth",
            "In production this would open the Microsoft OAuth2 web flow.\n"
            "(Xdg-portal browser would launch here.)"
        )

    def _add_offline(self) -> None:
        name, ok = self._prompt_text("Offline Persona Name", "Enter persona username:")
        if ok and name:
            self._accounts.append({"name": name, "type": "Offline", "active": False})
            self._refresh_account_list()

    def _remove_account(self) -> None:
        row = self._account_list.currentRow()
        if row >= 0:
            del self._accounts[row]
            self._refresh_account_list()

    def _set_active(self) -> None:
        row = self._account_list.currentRow()
        if row >= 0:
            for acc in self._accounts:
                acc["active"] = False
            self._accounts[row]["active"] = True
            self._active_name_lbl.setText(self._accounts[row]["name"])
            self._active_type_lbl.setText(self._accounts[row]["type"] + " Account")
            self._refresh_account_list()

    def _upload_skin(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Skin PNG", os.path.expanduser("~"), "PNG Images (*.png)"
        )
        if path:
            QMessageBox.information(self, "Skin Upload", f"Skin queued:\n{path}")

    @staticmethod
    def _prompt_text(title: str, label: str) -> tuple[str, bool]:
        return QInputDialog.getText(None, title, label)


# ─────────────────────────────────────────────────────────────────────────────
# PANEL 4 — SYSTEM TUNING & RUNTIME MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

class SystemTuningPanel(QWidget):
    """
    Panel 4 — JVM memory sliders, Java runtime selector,
    display resolution and JVM flag overrides.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        title = QLabel("◫  System Tuning & Runtime")
        title.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 18px; font-weight: bold; font-family: Consolas;"
        )
        root.addWidget(title)
        root.addWidget(divider())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        inner = QVBoxLayout(container)
        inner.setSpacing(16)
        scroll.setWidget(container)
        root.addWidget(scroll)

        # ── RAM Allocation Matrix ─────────────────────────────────────────
        ram_group = QGroupBox("RAM Allocation Matrix")
        ram_layout = QVBoxLayout(ram_group)
        ram_layout.setSpacing(14)

        self._xmx_slider, xmx_row = self._make_slider(
            "Maximum Heap  (─Xmx)", 512, 16384, 4096, "MB"
        )
        self._xms_slider, xms_row = self._make_slider(
            "Minimum Heap  (─Xms)", 256, 4096,  512,  "MB"
        )
        ram_layout.addLayout(xmx_row)
        ram_layout.addLayout(xms_row)

        per_instance_chk = QCheckBox("Enable Per-Instance RAM Override")
        per_instance_chk.setStyleSheet(f"color: {C_TEXT_DIM};")
        ram_layout.addWidget(per_instance_chk)
        inner.addWidget(ram_group)

        # ── Java Runtime Selector ─────────────────────────────────────────
        java_group = QGroupBox("Java Runtime Selector")
        java_layout = QVBoxLayout(java_group)
        java_layout.setSpacing(10)

        java_header = QHBoxLayout()
        java_header.addWidget(QLabel("Detected JVM environments:"))
        refresh_btn = QPushButton("⟳ Refresh")
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self._refresh_java)
        java_header.addStretch()
        java_header.addWidget(refresh_btn)
        java_layout.addLayout(java_header)

        self._java_list = QListWidget()
        self._java_list.setFixedHeight(100)
        self._populate_java_list()
        java_layout.addWidget(self._java_list)

        dl_row = QHBoxLayout()
        dl_row.addWidget(QLabel("Auto-Download JDK:"))
        self._jdk_combo = QComboBox()
        self._jdk_combo.addItems(["OpenJDK 8", "OpenJDK 17", "OpenJDK 21"])
        dl_btn = accent_button("⬇  Download to Userspace")
        dl_btn.clicked.connect(self._download_jdk)
        dl_row.addWidget(self._jdk_combo)
        dl_row.addWidget(dl_btn)
        dl_row.addStretch()
        java_layout.addLayout(dl_row)
        inner.addWidget(java_group)

        # ── Display & JVM Flags ───────────────────────────────────────────
        flags_group = QGroupBox("Display Resolution & JVM Flags")
        flags_layout = QGridLayout(flags_group)
        flags_layout.setVerticalSpacing(10)
        flags_layout.setHorizontalSpacing(14)

        self._res_width  = QSpinBox(); self._res_width.setRange(640, 7680);  self._res_width.setValue(1920)
        self._res_height = QSpinBox(); self._res_height.setRange(480, 4320);  self._res_height.setValue(1080)
        self._jvm_flags  = QLineEdit()
        self._jvm_flags.setPlaceholderText(
            "-XX:+UseG1GC -XX:MaxGCPauseMillis=50 -Dfml.ignoreInvalidMinecraftCertificates=true"
        )
        self._fullscreen_chk = QCheckBox("Force Fullscreen")

        flags_layout.addWidget(QLabel("Width"),            0, 0)
        flags_layout.addWidget(self._res_width,            0, 1)
        flags_layout.addWidget(QLabel("Height"),           0, 2)
        flags_layout.addWidget(self._res_height,           0, 3)
        flags_layout.addWidget(self._fullscreen_chk,       0, 4)
        flags_layout.addWidget(QLabel("Extra JVM Flags"),  1, 0)
        flags_layout.addWidget(self._jvm_flags,            1, 1, 1, 4)
        inner.addWidget(flags_group)

        # ── Save button ───────────────────────────────────────────────────
        save_btn = accent_button("✓  Save All Runtime Configuration")
        save_btn.clicked.connect(self._save_config)
        inner.addWidget(save_btn)
        inner.addStretch()

    # ── Static helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _make_slider(
        label: str, min_val: int, max_val: int, default: int, unit: str
    ) -> tuple[QSlider, QHBoxLayout]:
        layout = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setFixedWidth(240)
        lbl.setStyleSheet(f"color: {C_TEXT_DIM}; font-size: 12px;")
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.setTickInterval((max_val - min_val) // 8)
        val_lbl = QLabel(f"{default} {unit}")
        val_lbl.setFixedWidth(80)
        val_lbl.setStyleSheet(f"color: {C_VIOLET}; font-weight: bold; font-size: 12px;")
        slider.valueChanged.connect(lambda v, vl=val_lbl, u=unit: vl.setText(f"{v} {u}"))
        layout.addWidget(lbl)
        layout.addWidget(slider, stretch=1)
        layout.addWidget(val_lbl)
        return slider, layout

    def _populate_java_list(self) -> None:
        self._java_list.clear()
        envs = [
            ("/usr/lib/jvm/java-21-openjdk",  "OpenJDK 21.0.3  [System]",  C_LIME),
            ("/usr/lib/jvm/java-17-openjdk",  "OpenJDK 17.0.11 [System]",  C_TEXT),
            ("~/.local/share/nethercore/jdks/java-8", "OpenJDK 8u412 [Managed]", C_TEXT_DIM),
        ]
        for path, label, color in envs:
            item = QListWidgetItem(f"  ☕  {label}   ›  {path}")
            item.setForeground(QColor(color))
            self._java_list.addItem(item)

    def _refresh_java(self) -> None:
        self._populate_java_list()

    def _download_jdk(self) -> None:
        jdk = self._jdk_combo.currentText()
        QMessageBox.information(
            self, "JDK Download",
            f"Initiating download of {jdk} to:\n"
            f"~/.local/share/nethercore/jdks/\n\n"
            "(DownloadWorker thread would handle extraction here.)"
        )

    def _save_config(self) -> None:
        QMessageBox.information(
            self, "Configuration Saved",
            f"Runtime configuration persisted:\n"
            f"  Xmx: {self._xmx_slider.value()} MB\n"
            f"  Xms: {self._xms_slider.value()} MB\n"
            f"  Resolution: {self._res_width.value()}×{self._res_height.value()}\n"
            f"  JVM Flags: {self._jvm_flags.text() or '(default)'}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# PANEL 5 — ENGINE TELEMETRY & LIFECYCLE CONTROLS
# ─────────────────────────────────────────────────────────────────────────────

class TelemetryPanel(QWidget):
    """
    Panel 5 — Live coloured terminal output, crash-log export,
    and the emergency kill-switch for frozen game processes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._active_proc:   Optional[subprocess.Popen]    = None
        self._monitor_worker: Optional[ProcessMonitorWorker] = None
        self._log_lines: list[str] = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        title = QLabel("◬  Engine Telemetry")
        title.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 18px; font-weight: bold; font-family: Consolas;"
        )
        root.addWidget(title)
        root.addWidget(divider())

        # ── Control bar ───────────────────────────────────────────────────
        ctrl_row = QHBoxLayout()

        self._instance_indicator = QLabel("No Active Instance")
        self._instance_indicator.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 12px; padding: 4px 10px; "
            f"background: {C_CARD}; border-radius: 5px; border: 1px solid {C_BORDER};"
        )

        self._kill_btn = danger_button("⚡ KILL PROCESS")
        self._kill_btn.setEnabled(False)
        self._kill_btn.clicked.connect(self._kill_process)

        export_btn = QPushButton("⬆  Export to mclo.gs")
        export_btn.clicked.connect(self._export_logs)

        clear_btn = QPushButton("⌫  Clear Terminal")
        clear_btn.clicked.connect(self._clear_terminal)

        ctrl_row.addWidget(self._instance_indicator)
        ctrl_row.addStretch()
        ctrl_row.addWidget(clear_btn)
        ctrl_row.addWidget(export_btn)
        ctrl_row.addWidget(self._kill_btn)
        root.addLayout(ctrl_row)

        # ── Terminal output ───────────────────────────────────────────────
        self._terminal = QTextEdit()
        self._terminal.setReadOnly(True)
        self._terminal.setLineWrapMode(QTextEdit.NoWrap)
        root.addWidget(self._terminal, stretch=1)

        # ── Legend strip ──────────────────────────────────────────────────
        legend_row = QHBoxLayout()
        for color, label in [
            (C_CYAN,    "● INFO"),
            (C_GOLD,    "● WARN"),
            (C_CRIMSON, "● ERROR"),
        ]:
            ll = QLabel(label)
            ll.setStyleSheet(f"color: {color}; font-size: 11px;")
            legend_row.addWidget(ll)
        legend_row.addStretch()
        root.addLayout(legend_row)

        # ── Seed with a welcome banner ────────────────────────────────────
        self._append_line("NETHER CORE Engine Telemetry — Ready.", "info")
        self._append_line("Launch an instance to begin streaming log output.", "info")

    # ── Public API ────────────────────────────────────────────────────────────

    def attach_process(self, proc: subprocess.Popen, instance_name: str) -> None:
        """Bind a live Popen process to this panel and start monitoring."""
        self._active_proc = proc
        self._instance_indicator.setText(f"▶ Running: {instance_name}")
        self._instance_indicator.setStyleSheet(
            f"color: {C_LIME}; font-size: 12px; padding: 4px 10px; "
            f"background: #0A2200; border-radius: 5px; border: 1px solid {C_LIME}66;"
        )
        self._kill_btn.setEnabled(True)

        self._monitor_worker = ProcessMonitorWorker(proc)
        self._monitor_worker.output_signal.connect(self._append_line)
        self._monitor_worker.finished_signal.connect(self._on_process_ended)
        self._monitor_worker.start()

    def append_log(self, message: str, level: str = "info") -> None:
        """External entry point for injecting log lines from other panels."""
        self._append_line(message, level)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _append_line(self, line: str, level: str = "info") -> None:
        color_map = {"info": C_CYAN, "warn": C_GOLD, "error": C_CRIMSON}
        color = color_map.get(level, C_CYAN)
        ts = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{ts}] {line}"
        self._log_lines.append(formatted)

        cursor = self._terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(formatted + "\n")
        self._terminal.setTextCursor(cursor)
        self._terminal.ensureCursorVisible()

    def _kill_process(self) -> None:
        if self._active_proc:
            try:
                self._active_proc.kill()
                self._append_line("⚡ SIGKILL sent — process forcibly terminated.", "error")
            except Exception as exc:
                self._append_line(f"Kill failed: {exc}", "error")
        self._reset_state()

    def _on_process_ended(self, exit_code: int) -> None:
        msg = f"Process exited with code {exit_code}."
        level = "info" if exit_code == 0 else "error"
        self._append_line(msg, level)
        self._reset_state()

    def _reset_state(self) -> None:
        self._active_proc = None
        self._kill_btn.setEnabled(False)
        self._instance_indicator.setText("No Active Instance")
        self._instance_indicator.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 12px; padding: 4px 10px; "
            f"background: {C_CARD}; border-radius: 5px; border: 1px solid {C_BORDER};"
        )

    def _export_logs(self) -> None:
        if not self._log_lines:
            QMessageBox.warning(self, "Empty Log", "No log data to export.")
            return
        full_log = "\n".join(self._log_lines)
        # In production: POST to https://api.mclo.gs/1/log and open result URL
        QMessageBox.information(
            self, "Export to mclo.gs",
            f"Log would be POSTed to https://api.mclo.gs/1/log\n"
            f"({len(self._log_lines)} lines captured)\n\n"
            "The returned URL would be opened in your browser."
        )

    def _clear_terminal(self) -> None:
        self._terminal.clear()
        self._log_lines.clear()
        self._append_line("Terminal cleared.", "info")


# ─────────────────────────────────────────────────────────────────────────────
# PANEL 6 — IN-GAME AI BOT AUTOMATION CONTROL DECK
# ─────────────────────────────────────────────────────────────────────────────

class AiBotPanel(QWidget):
    """
    Panel 6 — AI bot automation dashboard.
    Tracks bot state, accepts natural-language directives,
    and monitors API token consumption.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._bot_running   = False
        self._token_balance = 120_000
        self._token_max     = 200_000
        self._tick_timer    = QTimer(self)
        self._tick_timer.timeout.connect(self._simulate_bot_tick)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        title = QLabel("◐  AI Bot Automation Deck")
        title.setStyleSheet(
            f"color: {C_VIOLET}; font-size: 18px; font-weight: bold; font-family: Consolas;"
        )
        root.addWidget(title)
        root.addWidget(divider())

        content_row = QHBoxLayout()
        content_row.setSpacing(20)

        # ── Left: Control & Directive Console ────────────────────────────
        left = QVBoxLayout()

        # Status card
        status_card = card_widget()
        sc_layout = QHBoxLayout(status_card)
        sc_layout.setContentsMargins(16, 14, 16, 14)
        self._bot_status_lbl = QLabel("● IDLE")
        self._bot_status_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 16px; font-weight: bold; background: transparent;"
        )
        self._bot_mode_lbl = QLabel("Mode: Stand-by")
        self._bot_mode_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 12px; background: transparent;"
        )
        sc_layout.addWidget(self._bot_status_lbl)
        sc_layout.addStretch()
        sc_layout.addWidget(self._bot_mode_lbl)
        left.addWidget(status_card)

        # Toggle buttons
        toggle_row = QHBoxLayout()
        self._init_btn = success_button("▶  Initialize Routine")
        self._init_btn.setFixedHeight(42)
        self._init_btn.clicked.connect(self._start_bot)
        self._halt_btn = danger_button("■  Halt Operations")
        self._halt_btn.setFixedHeight(42)
        self._halt_btn.setEnabled(False)
        self._halt_btn.clicked.connect(self._stop_bot)
        toggle_row.addWidget(self._init_btn)
        toggle_row.addWidget(self._halt_btn)
        left.addLayout(toggle_row)

        # Activity log
        left.addWidget(section_label("Bot Activity Feed", C_TEXT_DIM))
        self._bot_log = QTextEdit()
        self._bot_log.setReadOnly(True)
        left.addWidget(self._bot_log, stretch=1)

        # Directive input
        left.addWidget(section_label("Natural Language Directive", C_CYAN))
        directive_row = QHBoxLayout()
        self._directive_edit = QLineEdit()
        self._directive_edit.setPlaceholderText(
            "e.g. 'Navigate to the nearest village and gather wheat…'"
        )
        self._directive_edit.returnPressed.connect(self._send_directive)
        send_btn = accent_button("⟶  Send")
        send_btn.setFixedWidth(100)
        send_btn.clicked.connect(self._send_directive)
        directive_row.addWidget(self._directive_edit, stretch=1)
        directive_row.addWidget(send_btn)
        left.addLayout(directive_row)
        content_row.addLayout(left, stretch=3)

        # ── Right: Token Consumption Meter ────────────────────────────────
        right = QVBoxLayout()
        right.addWidget(section_label("Token Balance", C_GOLD))

        meter_card = card_widget()
        meter_card.setFixedWidth(200)
        mc_layout = QVBoxLayout(meter_card)
        mc_layout.setContentsMargins(16, 16, 16, 16)
        mc_layout.setSpacing(10)
        mc_layout.setAlignment(Qt.AlignCenter)

        self._token_arc_lbl = QLabel()
        self._token_arc_lbl.setFixedSize(120, 120)
        self._token_arc_lbl.setAlignment(Qt.AlignCenter)
        self._update_token_arc()
        mc_layout.addWidget(self._token_arc_lbl, alignment=Qt.AlignCenter)

        self._token_count_lbl = QLabel(f"{self._token_balance:,}")
        self._token_count_lbl.setAlignment(Qt.AlignCenter)
        self._token_count_lbl.setStyleSheet(
            f"color: {C_GOLD}; font-size: 18px; font-weight: bold; background: transparent;"
        )
        mc_layout.addWidget(self._token_count_lbl)

        self._token_bar = QProgressBar()
        self._token_bar.setRange(0, self._token_max)
        self._token_bar.setValue(self._token_balance)
        self._token_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"stop:0 #B8860B, stop:1 {C_GOLD}); }}"
        )
        mc_layout.addWidget(self._token_bar)

        tokens_lbl = QLabel("API Tokens Remaining")
        tokens_lbl.setAlignment(Qt.AlignCenter)
        tokens_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 10px; background: transparent;"
        )
        mc_layout.addWidget(tokens_lbl)

        right.addWidget(meter_card, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Instance binding
        right.addSpacing(14)
        right.addWidget(section_label("Bound Instance", C_TEXT_DIM))
        self._bound_combo = QComboBox()
        self._bound_combo.addItems(["Survival Hardcore", "Create Automation", "Dev Sandbox"])
        right.addWidget(self._bound_combo)
        right.addStretch()
        content_row.addLayout(right, stretch=1)

        root.addLayout(content_row, stretch=1)

        # Seed with startup message
        self._log_bot("AI Bot Controller ready. Awaiting directives.", "info")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _start_bot(self) -> None:
        self._bot_running = True
        self._bot_status_lbl.setText("● ACTIVE")
        self._bot_status_lbl.setStyleSheet(
            f"color: {C_LIME}; font-size: 16px; font-weight: bold; background: transparent;"
        )
        self._bot_mode_lbl.setText(f"Instance: {self._bound_combo.currentText()}")
        self._init_btn.setEnabled(False)
        self._halt_btn.setEnabled(True)
        self._tick_timer.start(2000)
        self._log_bot("▶  Bot routine initialised — monitoring game state…", "info")

    def _stop_bot(self) -> None:
        self._bot_running = False
        self._tick_timer.stop()
        self._bot_status_lbl.setText("● IDLE")
        self._bot_status_lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 16px; font-weight: bold; background: transparent;"
        )
        self._bot_mode_lbl.setText("Mode: Stand-by")
        self._init_btn.setEnabled(True)
        self._halt_btn.setEnabled(False)
        self._log_bot("■  Bot halted by operator command.", "warn")

    def _send_directive(self) -> None:
        directive = self._directive_edit.text().strip()
        if not directive:
            return
        self._log_bot(f"⟶  Directive received: '{directive}'", "info")
        self._log_bot("   Parsing NLP intent…", "info")
        self._log_bot("   Queuing sub-tasks for execution.", "info")
        self._directive_edit.clear()
        # Consume tokens
        cost = min(len(directive) * 4, self._token_balance)
        self._token_balance -= cost
        self._update_token_display()

    def _simulate_bot_tick(self) -> None:
        """Periodic fake telemetry while the bot is running."""
        import random
        events = [
            "Scanned 64 blocks in grid sector 3x3.",
            "Resource node detected: Iron Ore (×12).",
            "Path-finding recalculated — obstacle at (120, 64, -88).",
            "Inventory: 24/36 slots occupied.",
            "Crafting queue: 4 pending recipes.",
        ]
        self._log_bot(random.choice(events), "info")
        token_drain = 50
        self._token_balance = max(0, self._token_balance - token_drain)
        self._update_token_display()
        if self._token_balance == 0:
            self._log_bot("⚠  Token balance depleted — bot halted.", "warn")
            self._stop_bot()

    def _log_bot(self, message: str, level: str = "info") -> None:
        color_map = {"info": C_CYAN, "warn": C_GOLD, "error": C_CRIMSON}
        color = color_map.get(level, C_CYAN)
        ts = datetime.now().strftime("%H:%M:%S")
        cursor = self._bot_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(f"[{ts}] {message}\n")
        self._bot_log.setTextCursor(cursor)
        self._bot_log.ensureCursorVisible()

    def _update_token_display(self) -> None:
        self._token_count_lbl.setText(f"{self._token_balance:,}")
        self._token_bar.setValue(self._token_balance)
        pct = self._token_balance / self._token_max
        if pct < 0.2:
            color = C_CRIMSON
        elif pct < 0.5:
            color = C_GOLD
        else:
            color = C_LIME
        self._token_count_lbl.setStyleSheet(
            f"color: {color}; font-size: 18px; font-weight: bold; background: transparent;"
        )
        self._update_token_arc(pct)

    def _update_token_arc(self, pct: float = 1.0) -> None:
        """
        Draw a simple arc-style token gauge using QPainter onto a QPixmap
        and display it in the label.
        """
        size   = 120
        pm     = QPixmap(size, size)
        pm.fill(QColor("transparent"))
        p      = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)

        # Track ring
        p.setPen(QColor(C_BORDER))
        pen = QPen(QColor(C_BORDER), 8)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.drawArc(QRect(10, 10, size - 20, size - 20), 230 * 16, -280 * 16)

        # Value arc
        pct_color = C_LIME if pct > 0.5 else (C_GOLD if pct > 0.2 else C_CRIMSON)
        val_pen = QPen(QColor(pct_color), 8)
        val_pen.setCapStyle(Qt.RoundCap)
        p.setPen(val_pen)
        p.drawArc(QRect(10, 10, size - 20, size - 20), 230 * 16, int(-280 * 16 * pct))

        # Centre percentage text
        p.setPen(QColor(C_TEXT))
        f = QFont("Consolas", 14)
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRect(0, 0, size, size), Qt.AlignCenter, f"{int(pct * 100)}%")

        p.end()
        self._token_arc_lbl.setPixmap(pm)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    """
    Anarchy Cyberpunk — Nether Core Main Application Window.
    Hosts the sidebar nav deck and the right-side panel stack.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ Nether Core  —  Minecraft Instance Manager")
        self.setMinimumSize(1280, 780)
        self.resize(1440, 860)
        self.setStyleSheet(GLOBAL_QSS)
        self._build_ui()
        self._connect_signals()
        self._apply_startup_animation()

    # ── UI Assembly ───────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        central.setStyleSheet(f"background: {C_BG};")
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────
        self._sidebar = SidebarWidget()
        root_layout.addWidget(self._sidebar)

        # ── Right workspace ───────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {C_BG};")

        self._panel_instance  = InstanceMatrixPanel()
        self._panel_addon     = AddonRepositoryPanel()
        self._panel_identity  = IdentityCenterPanel()
        self._panel_tuning    = SystemTuningPanel()
        self._panel_telemetry = TelemetryPanel()
        self._panel_ai_bot    = AiBotPanel()

        for panel in [
            self._panel_instance,
            self._panel_addon,
            self._panel_identity,
            self._panel_tuning,
            self._panel_telemetry,
            self._panel_ai_bot,
        ]:
            self._stack.addWidget(panel)

        root_layout.addWidget(self._stack, stretch=1)

        # ── Status bar ────────────────────────────────────────────────────
        status = QStatusBar()
        self.setStatusBar(status)
        self._status_perm = QLabel(
            f"  ⚡ Nether Core v2.0  |  Python {sys.version.split()[0]}  |  "
            f"Bazzite/Fedora Silverblue"
        )
        self._status_perm.setStyleSheet(f"color: {C_TEXT_DIM};")
        self._clock_lbl = QLabel()
        self._clock_lbl.setStyleSheet(f"color: {C_VIOLET};")
        status.addPermanentWidget(self._status_perm)
        status.addPermanentWidget(self._clock_lbl)

        # Clock ticker
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start(1000)
        self._tick_clock()

    # ── Signal Wiring ─────────────────────────────────────────────────────────

    def _connect_signals(self) -> None:
        # Sidebar navigation → stack switching
        self._sidebar.nav_changed.connect(self._switch_panel)

        # Instance launch → start dummy process + show telemetry
        self._panel_instance.launch_requested.connect(self._handle_instance_launch)

    # ── Event Handlers ────────────────────────────────────────────────────────

    def _switch_panel(self, index: int) -> None:
        self._stack.setCurrentIndex(index)

    def _handle_instance_launch(self, instance_data: dict) -> None:
        """
        Called when the user clicks Launch on an instance card.
        In production this constructs the full JVM argument chain and
        spawns the Minecraft client process. Here we log the intent and
        switch to the telemetry panel.
        """
        name = instance_data.get("name", "Unknown")
        self._panel_telemetry.append_log(
            f"Preparing to launch: {name}  "
            f"(MC {instance_data.get('version')} / {instance_data.get('loader')})",
            "info"
        )
        self._panel_telemetry.append_log(
            "Constructing JVM argument chain…", "info"
        )
        self._panel_telemetry.append_log(
            "  java -Xmx4096M -Xms512M -XX:+UseG1GC … net.minecraft.client.main.Main",
            "info"
        )

        # Navigate to telemetry panel immediately
        self._sidebar._on_nav(4)   # index 4 = Engine Telemetry

        # In production, spawn the actual process here:
        # proc = subprocess.Popen([java_path, *jvm_args], stdout=subprocess.PIPE,
        #                         stderr=subprocess.STDOUT)
        # self._panel_telemetry.attach_process(proc, name)

        self._panel_telemetry.append_log(
            f"[Simulation] {name} would launch in a sandboxed flatpak/bwrap container.",
            "warn"
        )
        self._sidebar.set_status(f"▶ {name}", C_LIME)

    def _tick_clock(self) -> None:
        self._clock_lbl.setText(datetime.now().strftime("  %H:%M:%S   "))

    # ── Startup animation ─────────────────────────────────────────────────────

    def _apply_startup_animation(self) -> None:
        """Fade-in the window on startup via a window opacity animation."""
        self.setWindowOpacity(0.0)
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(500)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._fade_anim.start()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Application bootstrap. Call from your project's __main__.py or directly."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Apply a dark QPalette baseline so all Qt internals respect the theme
    palette = QPalette()
    for role, color in [
        (QPalette.Window,          C_BG),
        (QPalette.WindowText,      C_TEXT),
        (QPalette.Base,            C_CARD),
        (QPalette.AlternateBase,   C_CARD_HOVER),
        (QPalette.ToolTipBase,     C_CARD),
        (QPalette.ToolTipText,     C_TEXT),
        (QPalette.Text,            C_TEXT),
        (QPalette.Button,          C_CARD),
        (QPalette.ButtonText,      C_TEXT),
        (QPalette.BrightText,      "#FFFFFF"),
        (QPalette.Highlight,       C_VIOLET),
        (QPalette.HighlightedText, "#FFFFFF"),
        (QPalette.Link,            C_CYAN),
    ]:
        palette.setColor(role, QColor(color))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
