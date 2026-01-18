import shutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt
import humanize

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
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: 800; color: #1D1D1F;")
        layout.addWidget(title)

        subtitle = QLabel("Overview of your Mac's storage health.")
        subtitle.setStyleSheet("font-size: 15px; color: #86868B; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        # Storage Info Card
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E5E5;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        # Disk Icon & Label
        top_row = QHBoxLayout()
        icon_lbl = QLabel("💾")
        icon_lbl.setStyleSheet("font-size: 32px; border: none; background: transparent;")
        top_row.addWidget(icon_lbl)
        
        disk_lbl = QLabel("Macintosh HD")
        disk_lbl.setStyleSheet("font-size: 18px; font-weight: 600; color: #333; border: none;")
        top_row.addWidget(disk_lbl)
        top_row.addStretch()
        card_layout.addLayout(top_row)
        
        # Disk Usage Text
        self.usage_label = QLabel("Calculating...")
        self.usage_label.setStyleSheet("font-size: 14px; color: #555; border: none;")
        card_layout.addWidget(self.usage_label)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(12)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #F0F0F2;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 6px;
            }
        """)
        card_layout.addWidget(self.progress)
        
        layout.addWidget(self.card)

        # Refresh Stats
        self.refresh_stats()

    def refresh_stats(self):
        total, used, free = shutil.disk_usage("/")
        
        # Convert to readable format
        total_h = humanize.naturalsize(total, binary=True)
        used_h = humanize.naturalsize(used, binary=True)
        free_h = humanize.naturalsize(free, binary=True)
        percent = int((used / total) * 100)

        self.usage_label.setText(f"Used: {used_h}  |  Free: {free_h}  (Total: {total_h})")
        self.progress.setValue(percent)
