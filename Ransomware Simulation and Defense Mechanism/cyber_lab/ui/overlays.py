from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

class EducationOverlay(QWidget):
    """
    Displays educational context about current events.
    Appears as a 'toast' notification or overlay guidance.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.setFixedSize(300, 100)
        
        layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setStyleSheet("""
            background-color: rgba(16, 20, 30, 0.95);
            border: 1px solid #00ffea;
            border-radius: 10px;
            padding: 10px;
        """)
        
        container_layout = QVBoxLayout()
        
        self.title = QLabel("INFO")
        self.title.setStyleSheet("color: #00ffea; font-weight: bold; font-size: 14px;")
        
        self.message = QLabel("System Ready.")
        self.message.setWordWrap(True)
        self.message.setStyleSheet("color: #ecf0f1; font-size: 12px;")
        
        container_layout.addWidget(self.title)
        container_layout.addWidget(self.message)
        self.container.setLayout(container_layout)
        
        layout.addWidget(self.container)
        self.setLayout(layout)
        
        # Animations
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(500)
        
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.fade_out)
        self.hide_timer.setSingleShot(True)

    def show_message(self, title, text, duration=5000):
        self.title.setText(title)
        self.message.setText(text)
        
        # Position bottom right (relative to parent if possible, else screen)
        # For simplicity, we assume generic positioning or handled by main window
        # Here we just show it.
        
        self.show()
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.start()
        
        self.hide_timer.start(duration)

    def fade_out(self):
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.start()
        self.anim.finished.connect(self.hide)
