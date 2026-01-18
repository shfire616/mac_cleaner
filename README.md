# MacCleaner 🧹

> **The honest, open-source disk cleaner for macOS.**

![License](https://img.shields.io/badge/license-MIT-007AFF.svg?style=flat-square) ![Platform](https://img.shields.io/badge/platform-macOS-000000.svg?style=flat-square) ![Python](https://img.shields.io/badge/Built%20with-Python%20%26%20PyQt6-3776AB.svg?style=flat-square)

---

### 😫 **Tired of running out of disk space?** 
### 💸 **Tired of "free" cleaners that ask for a subscription to delete 1 file?**

**MacCleaner is for you.**

---

## ⚠️ **WARNING: USE AT YOUR OWN RISK** ⚠️
**MacCleaner is a powerful system utility. While it is designed to be safe by moving files to the Trash, the author is NOT responsible for any data loss, system instability, or accidental deletion of important files. Always ensure you have a full system backup (Time Machine) before performing any cleaning operations.**

---

No ads. No subscriptions. No hidden tracking. Just a simple, powerful tool to reclaim your hard drive space safely. Built by a developer, for everyone.

---

## 📸 Screenshots

| **Modern Dashboard** | **Smart Scanning** |
|:---:|:---:|
| ![Dashboard](https://raw.githubusercontent.com/shfire616/mac_cleaner/main/src/assets/dashboard_preview.png) | ![Scan Results](https://raw.githubusercontent.com/shfire616/mac_cleaner/main/src/assets/scan_preview.png) |
| *Visual overview of your disk usage* | *Grouped results for safe & easy cleaning* |

---

## ✨ Why MacCleaner?

*   **💯 100% Free & Open Source:** The code is right here. No secrets.
*   **🛡️ Safety First:** We don't just "delete" files. We move them to the **Trash 🗑️**, so you can always change your mind.
*   **🚀 Native Performance:** Built with PyQt6 to look and feel like a native macOS app.
*   **🧠 Smart Detection:** Automatically finds orphaned files from apps you uninstalled years ago.

## 🔍 Features

*   **📊 Dashboard:** See exactly how much space you have left at a glance.
*   **🧹 System Junk:** Safely clear `Caches`, `Logs`, and `Xcode DerivedData` (a lifesaver for developers!).
*   **🐘 Large Files:** Instantly spot the massive files clogging up your Downloads folder (>100MB).
*   **🗑️ App Leftovers:** Our smart engine scans `Application Support` to find junk left behind by deleted apps.
*   **🛠️ System Tools:** 
    *   **Update Cleaner:** Remove old macOS installer packages.
    *   **Time Machine Snapshots:** The #1 cause of hidden "System Data" bloat.

---

## 📦 Download & Install

### For Users
1.  Download the latest **MacCleaner.dmg** from the [Releases Page](https://github.com/shfire616/mac_cleaner/releases).
2.  Open the file and drag **MacCleaner** to your **Applications** folder.
3.  **First Run:** If macOS says the app is "unidentified":
    *   **Right-click** the App icon.
    *   Select **Open**.
    *   Click **Open** in the dialog box. (You only have to do this once!)

---

## 👨‍💻 For Developers

Want to tweak the code? Build it yourself?

### Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/mac_cleaner.git
cd mac_cleaner

# Create environment
conda create -n mac_cleaner python=3.11 -y
conda activate mac_cleaner

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/main.py
```

### Build Your Own DMG
```bash
# Install builder tools
pip install pyinstaller dmgbuild

# Build the App Bundle
pyinstaller --name="MacCleaner" --windowed --noconfirm --clean --paths=src src/main.py

# Create the DMG Installer
dmgbuild -s dmg_settings.py "MacCleaner" dist/MacCleaner.dmg
```

---

## ⚠️ Disclaimer

**Your data is your responsibility.**
MacCleaner is designed to be safe (using the Trash), but always ensure you have a backup (Time Machine) before performing system maintenance. The author provides this software "as is" without warranty.

## 📄 License

MIT License. Copyright © 2026 William Tam.
Free to use, modify, and distribute.
