from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel
from PyQt6.QtCore import Qt
import os

from src.ui.sidebar import Sidebar
from src.ui.dashboard import Dashboard
from src.ui.scan_view import ScanView
from src.ui.tools_view import ToolsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MacCleaner")
        self.resize(900, 600)
        
        # Central Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_selected.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)

        # Content Area (Stacked)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: white;")
        main_layout.addWidget(self.stack)

        # Initialize Pages
        self.dashboard = Dashboard()
        self.stack.addWidget(self.dashboard)

        # System Junk Page
        system_paths = [
            os.path.expanduser("~/Library/Caches"),
            os.path.expanduser("~/Library/Logs"),
            os.path.expanduser("~/Library/Developer/Xcode/DerivedData"),
            os.path.expanduser("~/Library/Developer/Xcode/Archives"),
            os.path.expanduser("~/Library/Caches/com.apple.SoftwareUpdate")
        ]
        self.system_junk_view = ScanView("System Junk", system_paths, group_mode=True)
        self.stack.addWidget(self.system_junk_view)

        # App Leftovers Page
        self.app_leftovers_view = ScanView("App Leftovers", [], app_leftover_mode=True)
        self.stack.addWidget(self.app_leftovers_view)

        # Large Files
        large_files_paths = [os.path.expanduser("~/Downloads")]
        self.large_files_view = ScanView("Large Files (Downloads > 100MB)", large_files_paths, min_size=100*1024*1024)
        self.stack.addWidget(self.large_files_view)

        # Tools Page
        self.tools_view = ToolsView()
        self.stack.addWidget(self.tools_view)

    def create_placeholder(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 20px; color: #888;")
        return lbl

    def switch_page(self, index, name):
        self.stack.setCurrentIndex(index)
