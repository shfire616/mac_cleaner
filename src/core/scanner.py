import os
from PyQt6.QtCore import QThread, pyqtSignal

class ScanWorker(QThread):
    item_found = pyqtSignal(str, int)
    scan_finished = pyqtSignal()
    progress_update = pyqtSignal(str)

    def __init__(self, target_paths, min_size=0, group_mode=False, app_leftover_mode=False):
        super().__init__()
        self.target_paths = target_paths
        self.min_size = min_size
        self.group_mode = group_mode
        self.app_leftover_mode = app_leftover_mode
        self._is_running = True

    def run(self):
        if self.app_leftover_mode:
            self.scan_app_leftovers()
        else:
            for path in self.target_paths:
                path = os.path.expanduser(path)
                if not os.path.exists(path):
                    continue
                if self.group_mode:
                    self.scan_grouped(path)
                else:
                    self.scan_individual(path)
        
        self.scan_finished.emit()

    def scan_app_leftovers(self):
        """Find folders in Application Support that don't have a corresponding app."""
        # 1. Get list of installed apps and split them into keywords
        # e.g., "Brave Browser" -> ["brave", "browser"]
        app_keywords = set()
        for app in os.listdir('/Applications'):
            if app.endswith('.app'):
                name = app.replace('.app', '').lower()
                # Split by space and common separators
                parts = name.replace('-', ' ').replace('_', ' ').split()
                for part in parts:
                    if len(part) > 2: # Ignore very short words like "to", "of"
                        app_keywords.add(part)

        # 2. Check Application Support
        support_path = os.path.expanduser("~/Library/Application Support")
        if not os.path.exists(support_path):
            return

        try:
            with os.scandir(support_path) as it:
                for entry in it:
                    if not self._is_running: return
                    if not entry.is_dir(): continue
                    
                    self.progress_update.emit(entry.name)
                    
                    folder_name = entry.name.lower()
                    
                    # Improved Matching Logic:
                    is_matched = False
                    
                    # Check if folder name contains any of the app keywords
                    for kw in app_keywords:
                        if kw in folder_name:
                            is_matched = True
                            break
                    
                    # Extra check: if app keywords contains the folder name
                    # (e.g. App is "Microsoft Outlook", folder is "Outlook")
                    if not is_matched:
                        for kw in folder_name.replace('.', ' ').split():
                            if len(kw) > 2 and kw in app_keywords:
                                is_matched = True
                                break

                    if not is_matched:
                        size = self.get_folder_size(entry.path)
                        if size > 0:
                            self.item_found.emit(entry.path, size)
        except Exception as e:
            print(f"Error scanning leftovers: {e}")

    def scan_individual(self, start_path):
        for root, dirs, files in os.walk(start_path):
            if not self._is_running: return
            self.progress_update.emit(root)
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    if os.path.islink(file_path): continue
                    size = os.path.getsize(file_path)
                    if size >= self.min_size:
                        self.item_found.emit(file_path, size)
                except: continue

    def scan_grouped(self, start_path):
        try:
            with os.scandir(start_path) as it:
                for entry in it:
                    if not self._is_running: return
                    self.progress_update.emit(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        size = self.get_folder_size(entry.path)
                        if size > 0: self.item_found.emit(entry.path, size)
                    elif entry.is_file(follow_symlinks=False):
                        if entry.stat().st_size >= self.min_size:
                            self.item_found.emit(entry.path, entry.stat().st_size)
        except: pass

    def get_folder_size(self, folder_path):
        total = 0
        try:
            for root, dirs, files in os.walk(folder_path):
                if not self._is_running: return 0
                for f in files:
                    fp = os.path.join(root, f)
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
        except: pass
        return total

    def stop(self):
        self._is_running = False