import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
import humanize

class ToolsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("System Tools (Advanced)")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = QLabel("These items require Admin permissions (sudo). We provide the commands for you.")
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)

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

    def add_tool_card(self, parent_layout, title, description, check_func, command):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E5E5;
                border-radius: 12px;
            }
        """)
        flayout = QVBoxLayout(frame)
        flayout.setContentsMargins(20, 20, 20, 20)
        flayout.setSpacing(10)
        
        # Header
        head = QHBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: 700; font-size: 15px; border: none; color: #1D1D1F;")
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
        lbl_desc.setStyleSheet("color: #86868B; border: none; font-size: 13px;")
        flayout.addWidget(lbl_desc)

        # Status Label
        status_lbl = QLabel("Status: Unknown")
        status_lbl.setStyleSheet("color: #007AFF; font-weight: 600; margin-top: 5px; border: none;")
        flayout.addWidget(status_lbl)

        # Command Area
        cmd_box = QFrame()
        cmd_box.setStyleSheet("background-color: #F5F5F7; border-radius: 6px; border: none;")
        cmd_layout = QHBoxLayout(cmd_box)
        cmd_layout.setContentsMargins(12, 8, 12, 8)
        
        lbl_cmd = QLabel(command)
        lbl_cmd.setStyleSheet("font-family: 'Menlo', 'Monaco', 'Courier New', monospace; color: #333; border: none; font-size: 12px;")
        cmd_layout.addWidget(lbl_cmd)
        
        btn_copy = QPushButton("Copy")
        btn_copy.setFixedWidth(70)
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.clicked.connect(lambda: self.copy_to_clipboard(command))
        cmd_layout.addWidget(btn_copy)
        
        flayout.addWidget(cmd_box)
        parent_layout.addWidget(frame)

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
