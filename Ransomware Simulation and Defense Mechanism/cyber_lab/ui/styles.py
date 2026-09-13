# VISION UI THEME - CRYPTOGUARD DARK GLASS EDITION (INDEX.HTML MATCHED)

VISION_UI_STYLE = """
/* GLOBAL WINDOW AND BASE WIDGETS */
QMainWindow {
    background-color: #020617;
}

QWidget {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 12px;
    color: #94a3b8;
}

/* TOP TOOLBAR / HEADER METRICS BAR */
QFrame#TopMetricsBar {
    background-color: rgba(2, 6, 23, 0.9);
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
    padding: 6px 12px;
}

QLabel#HeaderMetricTitle {
    color: #00e5ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

QLabel#HeaderMetricValue {
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
}

/* SIDEBAR NAVIGATION */
QFrame#SideBar {
    background-color: rgba(2, 6, 23, 0.95);
    border-right: 1px solid rgba(0, 212, 255, 0.2);
}

QFrame#UserProfileCard {
    background-color: rgba(4, 13, 33, 0.82);
    border-radius: 10px;
    padding: 10px;
    border: 1px solid rgba(0, 212, 255, 0.25);
}

/* SIDEBAR NAV BUTTONS */
QPushButton#NavBtn {
    border: 1px solid transparent;
    background-color: transparent;
    padding: 10px 14px;
    font-size: 13px;
    color: #94a3b8;
    text-align: left;
    border-radius: 8px;
    margin: 2px 8px;
    font-weight: 500;
}

QPushButton#NavBtn:hover {
    background-color: rgba(0, 212, 255, 0.08);
    color: #38bdf8;
    border: 1px solid rgba(0, 212, 255, 0.25);
}

QPushButton#NavBtn:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0066ff, stop:1 #00d4ff);
    color: #ffffff;
    border: 1px solid #00e5ff;
    font-weight: 700;
}

/* GENERAL BUTTONS */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0066ff, stop:1 #00d4ff);
    border: 1px solid rgba(0, 212, 255, 0.4);
    border-radius: 8px;
    padding: 8px 14px;
    color: #ffffff;
    text-align: center;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.5px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0052cc, stop:1 #00e5ff);
    border: 1px solid #00e5ff;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #0066ff;
}

/* HERO / ACTION BUTTONS */
QPushButton#HeroBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0066ff, stop:1 #00d4ff);
    border: 1px solid #00e5ff;
    border-radius: 8px;
    color: #ffffff;
    font-weight: 800;
    font-size: 13px;
    padding: 12px;
    letter-spacing: 1px;
}

QPushButton#HeroBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
    border: 1px solid #00ffaa;
}

/* CARDS & CONTAINERS */
QGroupBox, QFrame#CardPanel {
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 12px;
    margin-top: 15px;
    padding-top: 15px;
    background-color: rgba(4, 13, 33, 0.82);
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 0px;
    padding: 2px 8px;
    color: #00e5ff;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    background-color: transparent;
}

/* SCROLL AREA & CONTAINERS */
QScrollArea {
    background-color: #020617;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #020617;
}

/* LIST & PROCESS TABLES */
QListWidget, QTableWidget {
    background-color: rgba(2, 8, 22, 0.7);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 8px;
    color: #ffffff;
    padding: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    outline: none;
}

QListWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: rgba(0, 212, 255, 0.15);
    color: #00e5ff;
    border-left: 3px solid #00e5ff;
}

/* PROGRESS BARS */
QProgressBar {
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 6px;
    background-color: rgba(2, 8, 22, 0.8);
    text-align: center;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    height: 18px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0066ff, stop:1 #00ffaa);
    border-radius: 5px;
}

/* TYPOGRAPHY / LABELS */
QLabel {
    color: #94a3b8;
}

QLabel#Header {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
    margin-bottom: 10px;
}

QLabel#SubHeader {
    color: #38bdf8;
    font-size: 13px;
    margin-bottom: 8px;
    font-weight: 600;
}

/* TERMINAL LOGS & CODE INPUTS */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: rgba(2, 8, 22, 0.85);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 8px;
    color: #00ffaa;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #00e5ff;
}

/* SCROLLBARS */
QScrollBar:vertical {
    border: none;
    background: #020617;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 212, 255, 0.3);
    min-height: 20px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #00e5ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""