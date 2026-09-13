import random
import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from cyber_lab.ui import styles

class ParticleNetwork(QWidget):
    """
    Renders a floating particle network background.
    Nodes connect when close to each other, simulating network traffic/neural nets.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents) # Allow clicks through
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30) # ~30 FPS
        
        # Config
        self.count = 40
        self.connect_dist = 100
        self.color = QColor(0, 255, 234, 150) # Neon Cyan
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.init_particles()

    def init_particles(self):
        self.particles = []
        w, h = self.width(), self.height()
        for _ in range(self.count):
            self.particles.append({
                'x': random.uniform(0, w),
                'y': random.uniform(0, h),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.uniform(1.5, 3.5)
            })

    def update_particles(self):
        w, h = self.width(), self.height()
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Bounce
            if p['x'] < 0 or p['x'] > w: p['vx'] *= -1
            if p['y'] < 0 or p['y'] > h: p['vy'] *= -1
            
        self.update() # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Transparent background (parent widget handles bg color)
        
        pen = QPen(self.color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(QBrush(self.color))

        # Draw Particles & Connections
        for i, p1 in enumerate(self.particles):
            # Draw Node
            painter.drawEllipse(QPointF(p1['x'], p1['y']), p1['size'], p1['size'])
            
            # Connect to others
            for p2 in self.particles[i+1:]:
                dist = math.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])
                if dist < self.connect_dist:
                    alpha = int((1.0 - dist / self.connect_dist) * 100)
                    pen.setColor(QColor(0, 255, 234, alpha))
                    painter.setPen(pen)
                    painter.drawLine(QPointF(p1['x'], p1['y']), QPointF(p2['x'], p2['y']))

        painter.end()


class ScanlineOverlay(QWidget):
    """
    Renders horizontal scanlines for a CRT effect.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        # 1px line every 4px
        pen = QPen(QColor(0, 0, 0, 15)) # Reduced from 30 to 15 for better readability
        pen.setWidth(1)
        painter.setPen(pen)
        
        for y in range(0, self.height(), 4):
            painter.drawLine(0, y, self.width(), y)
        
        painter.end()
# Replace line 103 in animations.py with this:
stylesheet = ""

# VISION UI THEME - CRYPTOGUARD DARK EDITION (IMAGE MATCHED)

VISION_UI_STYLE = """
/* GLOBAL WINDOW AND BASE WIDGETS */
QMainWindow {
    background-color: #030712;
}

QWidget {
    font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    font-size: 12px;
    color: #94a3b8;
}

/* TOP TOOLBAR / HEADER METRICS BAR */
QFrame#TopMetricsBar {
    background-color: #080f1d;
    border-bottom: 1px solid #1e293b;
    padding: 6px 12px;
}

QLabel#HeaderMetricTitle {
    color: #64748b;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
}

QLabel#HeaderMetricValue {
    color: #00f2fe;
    font-size: 12px;
    font-weight: 700;
}

/* SIDEBAR NAVIGATION */
QFrame#SideBar {
    background-color: #080f1d;
    border-right: 1px solid #1e293b;
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
    background-color: #0f172a;
    color: #38bdf8;
    border: 1px solid #1e293b;
}

QPushButton#NavBtn:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #0369a1);
    color: #ffffff;
    border: 1px solid #00f2fe;
    font-weight: 700;
}

/* GENERAL BUTTONS */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f172a, stop:1 #1e293b);
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 14px;
    color: #38bdf8;
    text-align: center;
    font-weight: 600;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e293b, stop:1 #334155);
    border: 1px solid #00f2fe;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #0284c7;
}

/* HERO / ACTION BUTTONS */
QPushButton#HeroBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #0369a1);
    border: 1px solid #00f2fe;
    border-radius: 6px;
    color: #ffffff;
    font-weight: 700;
    font-size: 13px;
    padding: 10px;
}

QPushButton#HeroBtn:hover {
    background: #0284c7;
    border: 1px solid #38bdf8;
}

/* CARDS & CONTAINERS */
QGroupBox, QFrame#CardPanel {
    border: 1px solid #1e293b;
    border-radius: 10px;
    margin-top: 15px;
    padding-top: 15px;
    background-color: #080f1d;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 0px;
    padding: 2px 8px;
    color: #f8fafc;
    font-weight: 700;
    font-size: 13px;
    background-color: transparent;
}

/* SCROLL AREA & CONTAINERS */
QScrollArea {
    background-color: #030712;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #030712;
}

/* LIST & PROCESS TABLES */
QListWidget, QTableWidget {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 8px;
    color: #f8fafc;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid #0f172a;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: rgba(2, 132, 199, 0.2);
    color: #00f2fe;
    border-left: 3px solid #00f2fe;
}

/* PROGRESS BARS */
QProgressBar {
    border: 1px solid #1e293b;
    border-radius: 6px;
    background-color: #020617;
    text-align: center;
    color: #ffffff;
    font-weight: 600;
    height: 18px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #10b981);
    border-radius: 5px;
}

/* TYPOGRAPHY / LABELS */
QLabel {
    color: #94a3b8;
}

QLabel#Header {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 2px;
    margin-bottom: 10px;
}

QLabel#SubHeader {
    color: #00f2fe;
    font-size: 13px;
    margin-bottom: 8px;
    font-weight: 600;
}

/* TERMINAL LOGS & CODE INPUTS */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 6px;
    color: #10b981;
    font-family: 'Consolas', 'JetBrains Mono', 'Courier New', monospace;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #00f2fe;
}

/* SCROLLBARS */
QScrollBar:vertical {
    border: none;
    background: #030712;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #1e293b;
    min-height: 20px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #00f2fe;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

