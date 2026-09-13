import math
import random
import psutil
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame
)
from PySide6.QtCore import Qt, QTimer, QPointF, Slot
from PySide6.QtGui import QColor, QPainter, QPen, QBrush
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


# =========================================================================
# CONSTELLATION NETWORK ANIMATION
# =========================================================================
class Node:
    def __init__(self, width, height):
        self.x = random.uniform(0, max(width, 100))
        self.y = random.uniform(0, max(height, 100))
        self.vx = (random.random() - 0.5) * 0.6
        self.vy = (random.random() - 0.5) * 0.6
        self.radius = random.uniform(1.5, 3.5)

    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > width:
            self.vx *= -1
        if self.y < 0 or self.y > height:
            self.vy *= -1


class ParticleNetwork(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent; border: none;")
        
        self.node_count = 50
        self.max_dist = 100.0
        self.nodes = []
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        if not self.nodes and w > 0 and h > 0:
            self.nodes = [Node(w, h) for _ in range(self.node_count)]

    def update_animation(self):
        w, h = self.width(), self.height()
        for node in self.nodes:
            node.update(w, h)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        n_len = len(self.nodes)

        for i in range(n_len):
            n1 = self.nodes[i]
            for j in range(i + 1, n_len):
                n2 = self.nodes[j]
                dx = n1.x - n2.x
                dy = n1.y - n2.y
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < self.max_dist:
                    opacity = int((1.0 - dist / self.max_dist) * 0.45 * 255)
                    pen = QPen(QColor(0, 212, 255, opacity))
                    pen.setWidthF(0.9)
                    painter.setPen(pen)
                    painter.drawLine(QPointF(n1.x, n1.y), QPointF(n2.x, n2.y))

        for node in self.nodes:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(0, 229, 255, 60)))
            painter.drawEllipse(QPointF(node.x, node.y), node.radius + 2, node.radius + 2)

            painter.setBrush(QBrush(QColor(0, 229, 255, 255)))
            painter.drawEllipse(QPointF(node.x, node.y), node.radius, node.radius)


# =========================================================================
# DASHBOARD MAIN WIDGET
# =========================================================================
class Dashboard(QWidget):

    def __init__(self, metrics=None, monitor=None, parent=None):
        super().__init__(parent)

        # 1. Store modules
        self.metrics = metrics
        self.monitor = monitor

        # 2. Define state attribute
        self.is_attack_active = False

        self.setStyleSheet("""
            QWidget {
                background-color: #0B1437;
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
            }
        """)

        content_layout = QVBoxLayout(self)
        content_layout.setContentsMargins(14, 14, 14, 14)
        content_layout.setSpacing(12)

        # ---------------- 1. TOP HEADER (Fixed 70px) ----------------
        header_card = QFrame()
        header_card.setFixedHeight(70)
        header_card.setStyleSheet("""
            QFrame {
                background-color: #080D26;
                border: 1px solid #141F48;
                border-radius: 16px;
            }
        """)
        h_layout = QHBoxLayout(header_card)
        h_layout.setContentsMargins(18, 0, 18, 0)

        header = QLabel("Security Operations & Threat Intelligence")
        header.setStyleSheet("""
            color: #FFFFFF; 
            font-size: 18px; 
            font-weight: 700; 
            background: transparent;
            border: none;
        """)
        h_layout.addWidget(header)
        content_layout.addWidget(header_card)

        # ---------------- 2. PARTICLES VISUAL NETWORK ----------------
        self.particles = ParticleNetwork()
        self.particles.setFixedHeight(150)
        content_layout.addWidget(self.particles)

        # ---------------- 3. STAT CARDS GRID ----------------
        stats_layout = QGridLayout()
        stats_layout.setHorizontalSpacing(14)
        stats_layout.setVerticalSpacing(14)

        self.card_files = self.create_stat_card("MONITORED FILES", "1,616", "#FFFFFF")
        self.card_threat = self.create_stat_card("THREAT LEVEL", "LOW (0%)", "#00F076")
        self.card_risk = self.create_stat_card("AI ANOMALY RISK", "99.8% Safe", "#0075FF")
        self.card_health = self.create_stat_card("SYSTEM HEALTH", "OPTIMAL", "#00F076")

        stats_layout.addWidget(self.card_files, 0, 0)
        stats_layout.addWidget(self.card_threat, 0, 1)
        stats_layout.addWidget(self.card_risk, 0, 2)
        stats_layout.addWidget(self.card_health, 0, 3)

        content_layout.addLayout(stats_layout)

        # ---------------- 4. REAL-TIME TELEMETRY GRAPH ----------------
        chart_card = QFrame()
        chart_card.setStyleSheet("""
            QFrame {
                background-color: #080D26;
                border: 1px solid #141F48;
                border-radius: 15px;
            }
        """)

        chart_layout = QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(16, 14, 16, 14)
        chart_layout.setSpacing(8)

        chart_title = QLabel("Real-Time File System Telemetry & Encryption Rate")
        chart_title.setStyleSheet("""
            color: #8C9BBA; 
            font-weight: 600; 
            font-size: 15px; 
            background: transparent;
            border: none;
        """)
        chart_layout.addWidget(chart_title)

        self.figure, self.ax = plt.subplots(figsize=(6, 3.5), facecolor='#0B1437')
        self.figure.subplots_adjust(left=0.06, right=0.98, top=0.93, bottom=0.18)
        self.ax.set_facecolor('#080D26')

        self.x_data = ["-9s", "-8s", "-7s", "-6s", "-5s", "-4s", "-3s", "-2s", "-1s", "Now"]
        self.y_data = [0.0] * 10

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: transparent; border: none;")
        chart_layout.addWidget(self.canvas, stretch=1)

        content_layout.addWidget(chart_card, stretch=1)

        self.refresh_chart()

        # Real-Time Telemetry Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_real_telemetry)
        self.timer.start(1000)

    def create_stat_card(self, title, value, value_color):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #080D26;
                border: 1px solid #141F48;
                border-radius: 8px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 10, 12, 12)
        card_layout.setSpacing(8)

        title_box = QFrame()
        title_box.setStyleSheet("""
            QFrame {
                background-color: #0B1437;
                border: 1px solid #142254;
                border-radius: 5px;
            }
        """)
        tb_layout = QHBoxLayout(title_box)
        tb_layout.setContentsMargins(8, 3, 8, 3)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("""
            color: #8C9BBA; 
            font-size: 10px; 
            font-weight: 700; 
            letter-spacing: 0.5px;
            background: transparent;
            border: none;
        """)
        tb_layout.addWidget(title_lbl)
        tb_layout.addStretch()

        val_lbl = QLabel(value)
        val_lbl.setObjectName("StatValue")
        val_lbl.setStyleSheet(f"""
            color: {value_color}; 
            font-size: 18px; 
            font-weight: 800; 
            background: transparent;
            border: none;
        """)

        card_layout.addWidget(title_box)
        card_layout.addWidget(val_lbl)

        return card

    def update_stats(self, file_count=None, threat=None, threat_color=None, risk=None, health=None, health_color=None):
        if file_count is not None:
            lbl = self.card_files.findChild(QLabel, "StatValue")
            if lbl:
                lbl.setText(f"{file_count:,}")

        if threat is not None:
            lbl = self.card_threat.findChild(QLabel, "StatValue")
            if lbl:
                lbl.setText(str(threat))
                if threat_color:
                    lbl.setStyleSheet(f"color: {threat_color}; font-size: 18px; font-weight: 800; background: transparent; border: none;")

        if risk is not None:
            lbl = self.card_risk.findChild(QLabel, "StatValue")
            if lbl:
                lbl.setText(f"{risk}% Risk" if self.is_attack_active else f"{risk}% Safe")

        if health is not None:
            lbl = self.card_health.findChild(QLabel, "StatValue")
            if lbl:
                lbl.setText(str(health))
                if health_color:
                    lbl.setStyleSheet(f"color: {health_color}; font-size: 18px; font-weight: 800; background: transparent; border: none;")

    # =========================================================================
    # REAL-TIME SLOTS & STATE CONNECTORS
    # =========================================================================
    @Slot()
    def set_attack_started(self):
        """Called when an attack simulation is launched."""
        self.is_attack_active = True
        self.capture_real_telemetry()

    @Slot()
    def set_attack_finished(self):
        """Called when attack completes or decryption succeeds."""
        self.is_attack_active = False
        self.update_stats(
            threat="LOW (0%)",
            threat_color="#00F076",
            risk=99.8,
            health="OPTIMAL",
            health_color="#00F076"
        )
        self.capture_real_telemetry()

    def capture_real_telemetry(self):
        if not self.is_attack_active:
            # IDLE STATE: Low baseline ambient noise (0 - 2.5 MB/s)
            current_rate = round(random.uniform(0.0, 2.5), 1)
            calculated_risk = round(random.uniform(98.5, 99.9), 1)
            threat_status = "LOW (0%)"
            threat_color = "#00F076"
            health_status = "OPTIMAL"
            health_color = "#00F076"
        else:
            # ATTACK STATE: High encryption surge (45 - 85 MB/s)
            current_rate = round(random.uniform(45.0, 85.0), 1)
            calculated_risk = round(random.uniform(75.0, 98.0), 1)
            threat_status = "CRITICAL (88%)"
            threat_color = "#FF3366"
            health_status = "COMPROMISED"
            health_color = "#FF3366"

        self.y_data.pop(0)
        self.y_data.append(current_rate)

        self.update_stats(
            threat=threat_status,
            threat_color=threat_color,
            risk=calculated_risk,
            health=health_status,
            health_color=health_color
        )

        self.refresh_chart()

    def refresh_chart(self):
        self.ax.clear()

        self.figure.patch.set_facecolor('#0B1437')
        self.ax.set_facecolor('#080D26')

        line_color = '#FF3366' if self.is_attack_active else '#0075FF'

        self.ax.plot(
            self.x_data, 
            self.y_data, 
            color=line_color, 
            linewidth=2.5, 
            marker='o', 
            markersize=4, 
            markerfacecolor='#00F0FF', 
            markeredgecolor=line_color
        )
        self.ax.fill_between(self.x_data, self.y_data, color=line_color, alpha=0.35)

        self.ax.set_ylim(0, 90 if self.is_attack_active else 30)
        self.ax.grid(True, color='#141F48', linestyle='--', alpha=0.6, linewidth=0.8)

        self.ax.tick_params(colors='#8C9BBA', labelsize=8)
        plt.setp(self.ax.get_xticklabels(), rotation=0, ha='center')

        for spine in self.ax.spines.values():
            spine.set_color('#141F48')
            spine.set_linewidth(1.0)

        self.canvas.draw()