import os
import humanize
from send2trash import send2trash
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTreeWidget, QTreeWidgetItem, QLabel, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from src.core.scanner import ScanWorker

class ScanView(QWidget):
    def __init__(self, title, scan_paths, min_size=0, group_mode=False, app_leftover_mode=False):
        super().__init__()
        self.title = title
        self.scan_paths = scan_paths
        self.min_size = min_size
        self.group_mode = group_mode
        self.app_leftover_mode = app_leftover_mode
        self.total_size = 0
        self.items = {} # Map path -> QTreeWidgetItem

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # --- Header ---
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        title_lbl = QLabel(self.title)
        title_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #1D1D1F;")
        title_box.addWidget(title_lbl)
        
        self.status_lbl = QLabel("Ready to scan")
        self.status_lbl.setStyleSheet("color: #86868B; font-size: 13px;")
        title_box.addWidget(self.status_lbl)
        
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        
        self.scan_btn = QPushButton("Start Scan")
        # Direct style to ensure visibility
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #0062CC; }
            QPushButton:pressed { background-color: #004999; }
            QPushButton:disabled { background-color: #A0CFFF; color: #E6F2FF; }
        """)
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.setFixedWidth(120)
        self.scan_btn.clicked.connect(self.start_scan)
        header_layout.addWidget(self.scan_btn)
        
        layout.addLayout(header_layout)

        # --- Tree View (Card Style) ---
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["File / Folder", "Size"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.setAlternatingRowColors(False)
        self.tree.setRootIsDecorated(False)
        self.tree.setIndentation(20) # Flat list look for groups
        
        # Modern Tree Style
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #E5E5E5;
                border-radius: 8px;
                background-color: #FFFFFF;
                outline: none;
                padding: 5px;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
                color: #333;
            }
            QTreeWidget::item:selected {
                background-color: #F0F5FF;
                color: #007AFF;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #FFFFFF;
                color: #86868B;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #F0F0F0;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.tree)

        # --- Footer ---
        footer_layout = QHBoxLayout()
        
        self.total_lbl = QLabel("Total Found: 0 B")
        self.total_lbl.setStyleSheet("font-weight: 600; color: #1D1D1F; font-size: 14px;")
        footer_layout.addWidget(self.total_lbl)
        
        footer_layout.addStretch()
        
        self.clean_btn = QPushButton("Clean Selected")
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #D73328; }
            QPushButton:disabled { background-color: #FFD1CE; color: white; }
        """)
        self.clean_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clean_btn.setFixedWidth(140)
        self.clean_btn.clicked.connect(self.clean_selected)
        self.clean_btn.setEnabled(False)
        footer_layout.addWidget(self.clean_btn)
        
        layout.addLayout(footer_layout)

    def start_scan(self):
        self.tree.clear()
        self.items = {}
        self.total_size = 0
        self.update_total_label()
        
        self.scan_btn.setEnabled(False)
        self.clean_btn.setEnabled(False)
        self.status_lbl.setText("Scanning...")
        
        self.worker = ScanWorker(self.scan_paths, self.min_size, self.group_mode, self.app_leftover_mode)
        self.worker.item_found.connect(self.add_item)
        self.worker.scan_finished.connect(self.on_scan_finished)
        self.worker.progress_update.connect(self.on_progress)
        self.worker.start()

    def on_progress(self, path):
        short_path = path.split('/')[-1]
        self.status_lbl.setText(f"Scanning: {short_path}...")

    def add_item(self, path, size):
        self.total_size += size
        
        item = QTreeWidgetItem(self.tree)
        item.setText(0, path)
        item.setText(1, humanize.naturalsize(size))
        
        # Safety: App leftovers are unchecked by default to prevent accidental deletion
        if self.app_leftover_mode:
            item.setCheckState(0, Qt.CheckState.Unchecked)
        else:
            item.setCheckState(0, Qt.CheckState.Checked)
            
        item.setData(0, Qt.ItemDataRole.UserRole, path)
        item.setData(1, Qt.ItemDataRole.UserRole, size)
        
        self.items[path] = item
        self.update_total_label()

    def on_scan_finished(self):
        self.scan_btn.setEnabled(True)
        self.clean_btn.setEnabled(True)
        self.status_lbl.setText("Scan Complete")
        self.update_total_label()

    def update_total_label(self):
        self.total_lbl.setText(f"Total Found: {humanize.naturalsize(self.total_size)}")

    def clean_selected(self):
        selected_items = []
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            if item.checkState(0) == Qt.CheckState.Checked:
                selected_items.append(item)

        if not selected_items:
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete {len(selected_items)} items?\nThey will be moved to Trash.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            for item in selected_items:
                path = item.data(0, Qt.ItemDataRole.UserRole)
                try:
                    send2trash(path)
                    # Remove from tree
                    (item.parent() or root).removeChild(item)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {path}: {e}")
            
            QMessageBox.information(self, "Clean Complete", f"Successfully cleaned {deleted_count} items.")