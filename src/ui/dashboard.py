import shutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt
import humanize
from src.ui.styles import COLORS

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Title
        self.title_lbl = QLabel("Dashboard")
        layout.addWidget(self.title_lbl)

        self.subtitle_lbl = QLabel("Overview of your Mac's storage health.")
        layout.addWidget(self.subtitle_lbl)

        # Storage Info Card
        self.card = QFrame()
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        # Disk Icon & Label
        top_row = QHBoxLayout()
        self.icon_lbl = QLabel("💾")
        self.icon_lbl.setStyleSheet("font-size: 32px; border: none; background: transparent;")
        top_row.addWidget(self.icon_lbl)
        
        self.disk_lbl = QLabel("Macintosh HD")
        top_row.addWidget(self.disk_lbl)
        top_row.addStretch()
        card_layout.addLayout(top_row)
        
        # Disk Usage Text
        self.usage_label = QLabel("Calculating...")
        card_layout.addWidget(self.usage_label)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(12)
        self.progress.setTextVisible(False)
        card_layout.addWidget(self.progress)
        
        layout.addWidget(self.card)

        self.apply_theme()

        # Refresh Stats
        self.refresh_stats()

    def apply_theme(self):
        self.title_lbl.setStyleSheet(f"font-size: 28px; font-weight: 800; color: {COLORS['text_main']};")
        self.subtitle_lbl.setStyleSheet(f"font-size: 15px; color: {COLORS['text_secondary']}; margin-bottom: 10px;")
        
        self.card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        
        self.disk_lbl.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['text_main']}; border: none;")
        self.usage_label.setStyleSheet(f"font-size: 14px; color: {COLORS['text_secondary']}; border: none;")
        
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {COLORS['pressed']};
                border-radius: 6px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 6px;
            }}
        """)

    def refresh_stats(self):
        total, used, free = shutil.disk_usage("/")
        
        # Convert to readable format
        total_h = humanize.naturalsize(total, binary=True)
        used_h = humanize.naturalsize(used, binary=True)
        free_h = humanize.naturalsize(free, binary=True)
        percent = int((used / total) * 100)

        self.usage_label.setText(f"Used: {used_h}  |  Free: {free_h}  (Total: {total_h})")
        self.progress.setValue(percent)
