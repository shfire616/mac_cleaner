# macOS Modern Theme Palette

THEMES = {
    "light": {
        "background": "#F5F5F7",  # Main window background
        "surface": "#FFFFFF",     # Cards / Sidebar
        "primary": "#007AFF",     # Accent Blue
        "text_main": "#1D1D1F",
        "text_secondary": "#86868B",
        "border": "#E5E5E5",
        "danger": "#FF3B30",
        "success": "#34C759",
        "hover": "#F5F5F7",
        "pressed": "#E5E5E5",
        "input_bg": "#FFFFFF",
        "scrollbar_handle": "#C1C1C1",
        "button_text": "#1D1D1F",
        "button_border": "#D1D1D1",
        "button_bg": "#FFFFFF",
        "button_hover": "#F9F9F9",
    },
    "dark": {
        "background": "#1E1E1E",  # Darker background
        "surface": "#2C2C2E",     # Cards / Sidebar
        "primary": "#0A84FF",     # Brighter Blue for dark mode
        "text_main": "#F5F5F7",
        "text_secondary": "#98989D",
        "border": "#38383A",
        "danger": "#FF453A",
        "success": "#30D158",
        "hover": "#3A3A3C",
        "pressed": "#48484A",
        "input_bg": "#1C1C1E",
        "scrollbar_handle": "#636366",
        "button_text": "#F5F5F7",
        "button_border": "#38383A",
        "button_bg": "#2C2C2E",
        "button_hover": "#3A3A3C",
    }
}

CURRENT_THEME_NAME = "light"
COLORS = THEMES[CURRENT_THEME_NAME].copy()

def get_sheet(theme_name):
    c = THEMES[theme_name]
    return f"""
    QMainWindow {{
        background-color: {c['background']};
    }}
    QWidget {{
        font-family: ".AppleSystemUIFont";
        font-size: 13px;
        color: {c['text_main']};
    }}
    
    /* Scrollbars */
    QScrollBar:vertical {{
        border: none;
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {c['scrollbar_handle']};
        min-height: 20px;
        border-radius: 4px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* Primary Button */
    QPushButton[class="primary"] {{
        background-color: {c['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 600;
        font-size: 13px;
    }}
    QPushButton[class="primary"]:hover {{
        background-color: {c['primary']}; 
        /* Opacity handled by Qt usually, or slightly lighter/darker manually. 
           For simplicity, using same color but relying on system highlight or slight alpha if possible,
           but here we can just map to a hover variant if we want. 
           Let's just use the primary color and opacity change or brightness. */
        border: 1px solid {c['primary']};
    }}
    QPushButton[class="primary"]:pressed {{
        background-color: {c['primary']};
        opacity: 0.8;
    }}
    QPushButton[class="primary"]:disabled {{
        background-color: {c['border']};
        color: {c['text_secondary']};
    }}

    /* Danger Button */
    QPushButton[class="danger"] {{
        background-color: {c['danger']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 600;
    }}
    QPushButton[class="danger"]:hover {{
        opacity: 0.9;
    }}

    /* Secondary/Normal Button */
    QPushButton {{
        background-color: {c['button_bg']};
        border: 1px solid {c['button_border']};
        border-radius: 6px;
        padding: 6px 12px;
        color: {c['button_text']};
    }}
    QPushButton:hover {{
        background-color: {c['button_hover']};
        border-color: {c['border']};
    }}
    QPushButton:pressed {{
        background-color: {c['pressed']};
    }}
    
    /* Tooltips */
    QToolTip {{
        background-color: {c['surface']};
        color: {c['text_main']};
        border: 1px solid {c['border']};
    }}
    
    /* Checkbox */
    QCheckBox {{
        spacing: 8px;
        color: {c['text_main']};
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {c['border']};
        border-radius: 4px;
        background: {c['input_bg']};
    }}
    QCheckBox::indicator:checked {{
        background-color: {c['primary']};
        border-color: {c['primary']};
    }}
    """

def apply_styles(app, theme="light"):
    global COLORS, CURRENT_THEME_NAME
    if theme not in THEMES:
        theme = "light"
    CURRENT_THEME_NAME = theme
    COLORS.clear()
    COLORS.update(THEMES[theme])
    app.setStyleSheet(get_sheet(theme))
