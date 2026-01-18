from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal, Qt

class Sidebar(QWidget):
    page_selected = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(220)
        # Translucent blurred background effect is hard in pure Qt, 
        # so we use a solid but slightly distinct color.
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F2; 
                border-right: 1px solid #E5E5E5;
            }
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                color: #444;
                font-size: 13px;
                margin: 2px 10px;
                background-color: transparent;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(0,0,0, 0.05);
            }
            QPushButton:checked {
                background-color: #007AFF;
                color: white;
                font-weight: 600;
            }
            QLabel {
                padding-left: 15px;
                margin-top: 15px;
                margin-bottom: 5px;
                font-size: 11px;
                font-weight: bold;
                color: #888;
                text-transform: uppercase;
                border: none;
                background: transparent;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(4)

        # App Title / Logo Area
        title = QLabel("MacCleaner")
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: 800; 
            color: #333; 
            padding-left: 20px; 
            margin-bottom: 10px;
            text-transform: none;
        """)
        layout.addWidget(title)

        self.buttons = []
        
        # Section 1: Overview
        layout.addWidget(QLabel("Overview"))
        self.add_nav_button("Dashboard", 0, checked=True, icon="📊")

        # Section 2: Cleaning
        layout.addWidget(QLabel("Cleaning"))
        self.add_nav_button("System Junk", 1, icon="🧹")
        self.add_nav_button("App Leftovers", 2, icon="🗑️")
        self.add_nav_button("Large Files", 3, icon="🐘")

        # Section 3: Advanced
        layout.addWidget(QLabel("Tools"))
        self.add_nav_button("System Tools", 4, icon="🛠️")

        layout.addStretch() 
        
        # Footer / Version
        ver = QLabel("v1.0.0")
        ver.setStyleSheet("margin-top: 0; padding-left: 20px; font-weight: normal; color: #aaa;")
        layout.addWidget(ver)

    def add_nav_button(self, text, index, checked=False, icon=""):
        # Combine icon and text
        display_text = f"  {icon}   {text}" if icon else text
        
        btn = QPushButton(display_text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.handle_click(index, btn))
        self.layout().addWidget(btn)
        self.buttons.append(btn)

    def handle_click(self, index, clicked_btn):
        for btn in self.buttons:
            btn.setChecked(btn == clicked_btn)
        self.page_selected.emit(index, clicked_btn.text().strip().split('   ')[-1]) # Strip icon for signal