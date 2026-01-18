import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
import humanize
from src.ui.styles import COLORS

class ToolsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        self.tool_widgets = []

        self.title_lbl = QLabel("System Tools (Advanced)")
        layout.addWidget(self.title_lbl)
        
        self.desc_lbl = QLabel("These items require Admin permissions (sudo). We provide the commands for you.")
        layout.addWidget(self.desc_lbl)

        # 1. Update Leftovers
        self.add_tool_card(
            layout,
            "macOS Update Leftovers",
            "Found in /Library/Updates. These are often old update packages.",
            self.check_updates_size,
            "sudo rm -rf /Library/Updates/*"
        )

        # 2. Local Snapshots
        self.add_tool_card(
            layout,
            "Time Machine Local Snapshots",
            "Hidden backups that take up 'System Data' space.",
            self.check_snapshots,
            "for d in $(tmutil listlocalsnapshotdates | grep \"-\"); do sudo tmutil deletelocalsnapshots $d; done"
        )
        
        self.apply_theme()

    def add_tool_card(self, parent_layout, title, description, check_func, command):
        frame = QFrame()
        flayout = QVBoxLayout(frame)
        flayout.setContentsMargins(20, 20, 20, 20)
        flayout.setSpacing(10)
        
        # Header
        head = QHBoxLayout()
        lbl_title = QLabel(title)
        head.addWidget(lbl_title)
        head.addStretch()
        
        btn_check = QPushButton("Check Status")
        # Standard button style handled by global CSS, but we can tweak if needed
        btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_check.clicked.connect(lambda: self.run_check(check_func, status_lbl))
        head.addWidget(btn_check)
        flayout.addLayout(head)

        # Description
        lbl_desc = QLabel(description)
        flayout.addWidget(lbl_desc)

        # Status Label
        status_lbl = QLabel("Status: Unknown")
        flayout.addWidget(status_lbl)

        # Command Area
        cmd_box = QFrame()
        cmd_layout = QHBoxLayout(cmd_box)
        cmd_layout.setContentsMargins(12, 8, 12, 8)
        
        lbl_cmd = QLabel(command)
        cmd_layout.addWidget(lbl_cmd)
        
        btn_copy = QPushButton("Copy")
        btn_copy.setFixedWidth(70)
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.clicked.connect(lambda: self.copy_to_clipboard(command))
        cmd_layout.addWidget(btn_copy)
        
        flayout.addWidget(cmd_box)
        parent_layout.addWidget(frame)
        
        self.tool_widgets.append({
            'frame': frame,
            'title': lbl_title,
            'desc': lbl_desc,
            'status': status_lbl,
            'cmd_box': cmd_box,
            'cmd_lbl': lbl_cmd
        })

    def apply_theme(self):
        self.title_lbl.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {COLORS['text_main']};")
        self.desc_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; margin-bottom: 10px;")
        
        for w in self.tool_widgets:
            w['frame'].setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['surface']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 12px;
                }}
            """)
            w['title'].setStyleSheet(f"font-weight: 700; font-size: 15px; border: none; color: {COLORS['text_main']};")
            w['desc'].setStyleSheet(f"color: {COLORS['text_secondary']}; border: none; font-size: 13px;")
            w['status'].setStyleSheet(f"color: {COLORS['primary']}; font-weight: 600; margin-top: 5px; border: none;")
            w['cmd_box'].setStyleSheet(f"background-color: {COLORS['background']}; border-radius: 6px; border: none;")
            w['cmd_lbl'].setStyleSheet(f"font-family: 'Menlo', 'Monaco', 'Courier New', monospace; color: {COLORS['text_main']}; border: none; font-size: 12px;")

    def run_check(self, func, label):
        label.setText("Checking...")
        QApplication.processEvents()
        result = func()
        label.setText(result)

    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Command copied to clipboard!\nPaste it in your Terminal.")

    def check_updates_size(self):
        path = "/Library/Updates"
        if not os.path.exists(path):
            return "Folder not found (Clean)"
        
        try:
            total_size = 0
            # Note: Might need permission to even read sizes, but usually read is ok
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            
            if total_size == 0:
                return "Folder is empty."
            return f"Found: {humanize.naturalsize(total_size)}"
        except PermissionError:
            return "Permission Denied (Requires sudo to check)"

    def check_snapshots(self):
        try:
            result = subprocess.run(['tmutil', 'listlocalsnapshotdates', '/'], capture_output=True, text=True)
            count = result.stdout.count('com.apple.TimeMachine')
            if count == 0:
                return "No local snapshots found."
            return f"Found {count} local snapshots."
        except Exception as e:
            return f"Error: {str(e)}"
