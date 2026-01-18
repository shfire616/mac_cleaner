from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel,
    QDialog, QDialogButtonBox, QVBoxLayout
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QAction, QActionGroup, QGuiApplication
import os

from src.ui.sidebar import Sidebar
from src.ui.dashboard import Dashboard
from src.ui.scan_view import ScanView
from src.ui.tools_view import ToolsView
from src.ui.styles import COLORS, apply_styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MacCleaner")
        self.resize(900, 600)

        self.settings = QSettings("MacCleaner", "MacCleaner")
        self.user_theme = self.settings.value("theme", "system")

        self.init_menu()

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

        self.apply_user_theme()

    def apply_theme(self):
        self.stack.setStyleSheet(f"background-color: {COLORS['background']};")
        if hasattr(self, 'sidebar'): self.sidebar.apply_theme()
        if hasattr(self, 'dashboard'): self.dashboard.apply_theme()
        if hasattr(self, 'tools_view'): self.tools_view.apply_theme()
        if hasattr(self, 'system_junk_view'): self.system_junk_view.apply_theme()
        if hasattr(self, 'app_leftovers_view'): self.app_leftovers_view.apply_theme()
        if hasattr(self, 'large_files_view'): self.large_files_view.apply_theme()


    def create_placeholder(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(f"font-size: 20px; color: {COLORS['text_secondary']};")
        return lbl

    def init_menu(self):
        menubar = self.menuBar()
        assert menubar is not None
        view_menu = menubar.addMenu("View")
        assert view_menu is not None
        theme_menu = view_menu.addMenu("Theme")
        assert theme_menu is not None

        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)

        self.theme_system_action = QAction("System", self)
        self.theme_system_action.setCheckable(True)
        self.theme_light_action = QAction("Light", self)
        self.theme_light_action.setCheckable(True)
        self.theme_dark_action = QAction("Dark", self)
        self.theme_dark_action.setCheckable(True)

        self.theme_action_group.addAction(self.theme_system_action)
        self.theme_action_group.addAction(self.theme_light_action)
        self.theme_action_group.addAction(self.theme_dark_action)

        theme_menu.addAction(self.theme_system_action)
        theme_menu.addAction(self.theme_light_action)
        theme_menu.addAction(self.theme_dark_action)

        self.theme_system_action.triggered.connect(lambda: self.set_user_theme("system"))
        self.theme_light_action.triggered.connect(lambda: self.set_user_theme("light"))
        self.theme_dark_action.triggered.connect(lambda: self.set_user_theme("dark"))

        if self.user_theme == "dark":
            self.theme_dark_action.setChecked(True)
        elif self.user_theme == "light":
            self.theme_light_action.setChecked(True)
        else:
            self.theme_system_action.setChecked(True)

        help_menu = menubar.addMenu("Help")
        assert help_menu is not None
        self.about_action = QAction("About MacCleaner", self)
        self.about_action.triggered.connect(self.show_about)
        help_menu.addAction(self.about_action)

    def apply_user_theme(self):
        if self.user_theme == "system":
            scheme = None
            style_hints = QGuiApplication.styleHints()
            if style_hints is not None:
                scheme = style_hints.colorScheme()
            theme = "dark" if scheme == Qt.ColorScheme.Dark else "light"
        else:
            theme = self.user_theme
        apply_styles(self, theme)
        if hasattr(self, "stack"):
            self.apply_theme()

    def set_user_theme(self, theme):
        self.user_theme = theme
        self.settings.setValue("theme", theme)
        self.apply_user_theme()

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About MacCleaner")
        dialog.setMinimumWidth(420)

        layout = QVBoxLayout(dialog)
        title = QLabel("MacCleaner")
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(title)

        desc = QLabel(
            "MacCleaner helps you scan for system junk, app leftovers, and large files to free up space."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        license_link = QLabel('<a href="https://opensource.org/licenses/MIT">MIT License</a>')
        license_link.setOpenExternalLinks(True)
        layout.addWidget(license_link)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.exec()

    def switch_page(self, index, name):
        self.stack.setCurrentIndex(index)
