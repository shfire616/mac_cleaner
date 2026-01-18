# macOS Modern Theme Palette

COLORS = {
    "background": "#F5F5F7",  # Main window background
    "surface": "#FFFFFF",     # Cards / Sidebar
    "primary": "#007AFF",     # Accent Blue
    "text_main": "#1D1D1F",
    "text_secondary": "#86868B",
    "border": "#E5E5E5",
    "danger": "#FF3B30",
    "success": "#34C759"
}

GLOBAL_STYLES = """
    QMainWindow {
        background-color: #F5F5F7;
    }
    QWidget {
        font-family: ".AppleSystemUIFont";
        font-size: 13px;
        color: #1D1D1F;
    }
    
    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 8px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background: #C1C1C1;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    /* Primary Button */
    QPushButton[class="primary"] {
        background-color: #007AFF;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 600;
        font-size: 13px;
    }
    QPushButton[class="primary"]:hover {
        background-color: #0062CC;
    }
    QPushButton[class="primary"]:pressed {
        background-color: #004999;
    }
    QPushButton[class="primary"]:disabled {
        background-color: #A0CFFF;
        color: #E6F2FF;
    }

    /* Danger Button */
    QPushButton[class="danger"] {
        background-color: #FF3B30;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 600;
    }
    QPushButton[class="danger"]:hover {
        background-color: #D73328;
    }

    /* Secondary/Normal Button */
    QPushButton {
        background-color: #FFFFFF;
        border: 1px solid #D1D1D1;
        border-radius: 6px;
        padding: 6px 12px;
        color: #1D1D1F;
    }
    QPushButton:hover {
        background-color: #F9F9F9;
        border-color: #C1C1C1;
    }
    QPushButton:pressed {
        background-color: #F0F0F0;
    }
"""

def apply_styles(app):
    app.setStyleSheet(GLOBAL_STYLES)
