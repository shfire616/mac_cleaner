import os
import humanize
from send2trash import send2trash
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTreeWidget, QTreeWidgetItem, QLabel, QMessageBox, QHeaderView,
    QCheckBox
)
from PyQt6.QtCore import Qt, QSignalBlocker, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence
from src.core.scanner import ScanWorker
from src.ui.styles import COLORS

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
        self._initial_size_set = False

        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # --- Header ---
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        self.title_lbl = QLabel(self.title)
        title_box.addWidget(self.title_lbl)
        
        self.status_lbl = QLabel("Ready to scan")
        title_box.addWidget(self.status_lbl)
        
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        
        self.scan_btn = QPushButton("Start Scan")
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.setFixedWidth(120)
        self.scan_btn.clicked.connect(self.start_scan)
        header_layout.addWidget(self.scan_btn)
        
        layout.addLayout(header_layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(False)
        self.tree.setColumnCount(2)
        
        self.tree.setHeaderLabels(["File / Folder", "Size"])
        header = self.tree.header()
        assert header is not None
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(False)
        
        self.tree.setAlternatingRowColors(False)
        self.tree.setRootIsDecorated(False)
        self.tree.setIndentation(20)
        
        layout.addWidget(self.tree)
        
        self.select_all_checkbox = QCheckBox(header)
        self.select_all_checkbox.setFixedWidth(20)
        self.select_all_checkbox.setTristate(True)
        self.select_all_checkbox.stateChanged.connect(self.on_select_all_state_changed)
        self.select_all_checkbox.show()
        
        header.geometriesChanged.connect(self.update_header_checkbox)
        header.sectionResized.connect(lambda i, o, n: self.update_header_checkbox())
        header.sectionMoved.connect(lambda i, o, n: self.update_header_checkbox())

        self.select_all_shortcut = QShortcut(QKeySequence.StandardKey.SelectAll, self)
        self.select_all_shortcut.activated.connect(self.select_all_items)

        self.tree.itemChanged.connect(self.on_item_check_changed)

        self.update_select_all_checkbox_state()

        # --- Footer ---
        footer_layout = QHBoxLayout()
        
        self.total_lbl = QLabel("Total Found: 0 B")
        footer_layout.addWidget(self.total_lbl)
        
        footer_layout.addStretch()
        
        self.clean_btn = QPushButton("Clean Selected")
        self.clean_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clean_btn.setFixedWidth(140)
        self.clean_btn.clicked.connect(self.clean_selected)
        self.clean_btn.setEnabled(False)
        footer_layout.addWidget(self.clean_btn)
        
        layout.addLayout(footer_layout)
        
        self.apply_theme()
        
        scrollbar = self.tree.horizontalScrollBar()
        assert scrollbar is not None
        scrollbar.valueChanged.connect(lambda val: self.update_header_checkbox())
        
        self.update_header_checkbox()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if not self._initial_size_set:
            QTimer.singleShot(0, self._set_column_sizes)

    def _set_column_sizes(self):
        if self._initial_size_set:
            return
            
        header = self.tree.header()
        if not header:
            return
            
        width = header.width()
        if width > 50:
            w0 = int(width * 0.8)
            w1 = width - w0
            header.resizeSection(0, w0)
            header.resizeSection(1, w1)
            self._initial_size_set = True

    def update_header_checkbox(self):
        header = self.tree.header()
        assert header is not None
        h = header.height()
        y = (h - 16) // 2
        
        x = header.sectionViewportPosition(0) + 8
        self.select_all_checkbox.move(x, y)

    def apply_theme(self):
        self.title_lbl.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {COLORS['text_main']};")
        self.status_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        
        self.scan_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {COLORS['primary']}; opacity: 0.9; }}
            QPushButton:pressed {{ background-color: {COLORS['pressed']}; }}
            QPushButton:disabled {{ background-color: {COLORS['border']}; color: {COLORS['text_secondary']}; }}
        """)
        
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                background-color: {COLORS['surface']};
                outline: none;
                padding: 0px;
            }}
            QTreeWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {COLORS['border']};
                color: {COLORS['text_main']};
            }}
            QTreeWidget::item:selected {{
                background-color: {COLORS['hover']};
                color: {COLORS['primary']};
                border-radius: 4px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['surface']};
                color: {COLORS['text_secondary']};
                padding: 6px;
                border: none;
                border-bottom: 2px solid {COLORS['border']};
                font-weight: 600;
                font-size: 11px;
                text-transform: uppercase;
            }}
            QHeaderView::section:first {{
                padding-left: 36px;
            }}
        """)
        
        self.total_lbl.setStyleSheet(f"font-weight: 600; color: {COLORS['text_main']}; font-size: 14px;")
        
        self.clean_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background-color: {COLORS['danger']}; opacity: 0.9; }}
            QPushButton:disabled {{ background-color: {COLORS['border']}; color: white; }}
        """)

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
        
        item.setCheckState(0, Qt.CheckState.Checked)            
        item.setData(0, Qt.ItemDataRole.UserRole, path)
        item.setData(1, Qt.ItemDataRole.UserRole, size)
        
        self.items[path] = item
        self.update_total_label()
        self.update_select_all_checkbox_state()

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
        if root is not None:
            for i in range(root.childCount()):
                item = root.child(i)
                if item is not None and item.checkState(0) == Qt.CheckState.Checked:
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
                    if root is not None:
                        (item.parent() or root).removeChild(item)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {path}: {e}")

    def on_select_all_state_changed(self, state):
        if state == Qt.CheckState.PartiallyChecked.value:
            return
        self.set_all_items_checked(state == Qt.CheckState.Checked.value)

    def select_all_items(self):
        self.set_all_items_checked(True)

    def set_all_items_checked(self, checked):
        root = self.tree.invisibleRootItem()
        if root is None:
            return
        with QSignalBlocker(self.tree):
            for i in range(root.childCount()):
                item = root.child(i)
                if item is not None:
                    item.setCheckState(0, Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
        self.update_select_all_checkbox_state()

    def on_item_check_changed(self, item, column):
        if column != 0:
            return
        self.update_select_all_checkbox_state()

    def update_select_all_checkbox_state(self):
        root = self.tree.invisibleRootItem()
        if root is None or root.childCount() == 0:
            self.select_all_checkbox.setCheckState(Qt.CheckState.Unchecked)
            return

        checked_count = 0
        total_count = root.childCount()
        for i in range(total_count):
            item = root.child(i)
            if item is not None and item.checkState(0) == Qt.CheckState.Checked:
                checked_count += 1

        with QSignalBlocker(self.select_all_checkbox):
            if checked_count == 0:
                self.select_all_checkbox.setCheckState(Qt.CheckState.Unchecked)
            elif checked_count == total_count:
                self.select_all_checkbox.setCheckState(Qt.CheckState.Checked)
            else:
                self.select_all_checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
