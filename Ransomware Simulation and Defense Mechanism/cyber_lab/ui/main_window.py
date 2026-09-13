import sys
import time
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QStackedWidget, QFrame, QLabel, QScrollArea
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSizePolicy

from .styles import VISION_UI_STYLE
from .animations import ParticleNetwork, ScanlineOverlay
from .overlays import EducationOverlay

from .dashboard import Dashboard
from .simulation_panel import SimulationPanel
from .defense_panel import DefensePanel
from .report_panel import ReportPanel
from .cyber_range_panel import CyberRangePanel
from .key_panel import KeyPanel
from .forensics_panel import ForensicsPanel


ENHANCED_CYBERGUARD_THEME = """
/* Global Application Dark Theme */
QMainWindow, QWidget {
    background-color: #030712;
    color: #f8fafc;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

/* Scroll Area Styling */
QScrollArea {
    background-color: #030712;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #030712;
}

/* Sidebar Container */
QFrame#SideBar {
    background-color: #060a12;
    border-right: 1px solid #101f42;
}

/* User Profile Glass Card */
QFrame#UserProfileCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0b1936, stop:1 #050c1a);
    border: 1px solid #1e293b;
    border-radius: 10px;
}

/* System Telemetry Realtime Status Card */
QFrame#SystemStatusCard {
    background-color: #050c1a;
    border: 1px solid #0f244a;
    border-radius: 10px;
}

/* Sidebar Navigation Buttons */
QPushButton#NavBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 13px;
    text-align: left;
}

QPushButton#NavBtn:hover {
    background-color: #0f172a;
    color: #f8fafc;
    border-left: 3px solid #0284c7;
}

QPushButton#NavBtn:checked {
    background-color: #0b1936;
    color: #00d2ff;
    border-left: 3px solid #00d2ff;
    font-weight: 700;
}

/* Universal Action Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f172a, stop:1 #1e293b);
    color: #38bdf8;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e293b, stop:1 #334155);
    border: 1px solid #38bdf8;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #0284c7;
}

/* Frame and Card Containers across Panels */
QFrame, QGroupBox {
    background-color: #080f1d;
    border: 1px solid #1e293b;
    border-radius: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #38bdf8;
    font-size: 13px;
    font-weight: 700;
}

/* Inputs, Code Displays & Logs */
QTextEdit, QPlainTextEdit, QLineEdit {
    background-color: #020617;
    color: #10b981;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
}

QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #38bdf8;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #030712;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #1e293b;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #38bdf8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


class MainWindow(QMainWindow):

    def __init__(self, core_modules):
        super().__init__()

        self.core = core_modules
        self.start_time = time.time()

        self.signal_frames = [
            "⚡ [ █ ░ ░ ░ ░ ░ █ ]",
            "⚡ [ ░ █ ░ ░ ░ █ ░ ]",
            "⚡ [ ░ ░ █ ░ █ ░ ░ ]",
            "⚡ [ ░ ░ ░ █ ░ ░ ░ ]",
            "⚡ [ ░ ░ █ ░ █ ░ ░ ]",
            "⚡ [ ░ █ ░ ░ ░ █ ░ ]"
        ]
        self.signal_idx = 0

        self.setWindowTitle("CryptoGuard — Ransomware Detection & Endpoint Response")
        self.resize(1280, 840)

        self.setStyleSheet(VISION_UI_STYLE + ENHANCED_CYBERGUARD_THEME)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content_stack = QStackedWidget()
        self.content_stack.setContentsMargins(15, 15, 15, 15)

        self.scroll_area.setWidget(self.content_stack)
        main_layout.addWidget(self.scroll_area)

        # Initialize Pages
        self.dashboard = Dashboard(self.core.get('metrics'), self.core.get('monitor'))
        self.simulation = SimulationPanel(
            self.core['sandbox'], 
            self.core['keys'], 
            self.core['encryption'], 
            self.core['decryption'],
            self.core.get('backup'),
            self.core.get('integrity'),
            self.core.get('simulator'),
            self.core.get('threat_intel'),
            self.core.get('mfa'),
            self.core.get('rbac'),
            self.core.get('audit')
        )
        self.defense = DefensePanel(
            self.core['monitor'], 
            self.core['defense'],
            self.core['logger'],
            self.core.get('threat_intel')
        )
        self.report_panel = ReportPanel(
            self.core['report_gen'],
            self.core['metrics']
        )
        self.cyber_range_panel = CyberRangePanel(
            self.core['cyber_range'],
            self.core['net_sim'],
            self.core['social_eng']
        )
        self.key_panel = KeyPanel(
            self.core['keys'],
            self.core['mfa']
        )
        self.forensics_panel = ForensicsPanel(
            self.core['pen_test'],
            self.core['forensics']
        )

        # Add Pages to Stack
        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.simulation)
        self.content_stack.addWidget(self.defense)
        self.content_stack.addWidget(self.report_panel)
        self.content_stack.addWidget(self.cyber_range_panel)
        self.content_stack.addWidget(self.key_panel)
        self.content_stack.addWidget(self.forensics_panel)

        # Explicitly set Dashboard (Index 0) as the initial active page
        self.content_stack.setCurrentIndex(0)

        # Direct Signal Hooks
        if hasattr(self.simulation, 'attack_started'):
            self.simulation.attack_started.connect(self._on_attack_launched)
        if hasattr(self.simulation, 'attack_stopped'):
            self.simulation.attack_stopped.connect(self._on_attack_restored)

        for btn_attr in ['btn_launch', 'btn_attack', 'launch_btn']:
            if hasattr(self.simulation, btn_attr):
                getattr(self.simulation, btn_attr).clicked.connect(self._on_attack_launched)

        for btn_attr in ['btn_restore', 'btn_decrypt', 'restore_btn']:
            if hasattr(self.simulation, btn_attr):
                getattr(self.simulation, btn_attr).clicked.connect(self._on_attack_restored)

        if hasattr(self.defense, 'risk_changed'):
            self.defense.risk_changed.connect(lambda risk_val: self.update_global_threat_level(int(risk_val * 100)))

        self.setCentralWidget(main_widget)

        self.overlay = EducationOverlay(self)
        self.overlay.move(self.width() - 330, self.height() - 130)
        self.overlay.show_message("CryptoGuard Active", "System initialized and protected. Select a tab to monitor operations.")

        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.setInterval(1000)
        self.telemetry_timer.timeout.connect(self.update_realtime_telemetry)
        self.telemetry_timer.start()

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()
        self.activateWindow()

        QTimer.singleShot(500, self._release_topmost_lock)

    def update_global_threat_level(self, risk_percent):
        """Synchronizes Defense Center Risk Score directly to Dashboard UI."""
        if risk_percent > 15:
            self.dashboard.is_attack_active = True
            
            if risk_percent > 70:
                threat_str = f"CRITICAL ({risk_percent}%)"
                threat_color = "#FF3366"
                health_str = "COMPROMISED"
            else:
                threat_str = f"ELEVATED ({risk_percent}%)"
                threat_color = "#F59E0B"
                health_str = "WARNING"

            self.dashboard.update_stats(
                threat=threat_str,
                threat_color=threat_color,
                risk=risk_percent,
                health=health_str,
                health_color=threat_color
            )

            if hasattr(self, 'state_txt'):
                self.state_txt.setText("UNDER ATTACK")
                self.state_txt.setStyleSheet("color: #ef4444; font-size: 13px; font-weight: 800; border: none;")
        else:
            self.dashboard.is_attack_active = False
            if hasattr(self.dashboard, 'set_attack_finished'):
                self.dashboard.set_attack_finished()
            else:
                self.dashboard.update_stats(
                    threat="LOW (0%)",
                    threat_color="#00F076",
                    risk=99.8,
                    health="OPTIMAL",
                    health_color="#00F076"
                )

            if hasattr(self, 'state_txt'):
                self.state_txt.setText("Protected")
                self.state_txt.setStyleSheet("color: #10b981; font-size: 13px; font-weight: 800; border: none;")

    def _on_attack_launched(self):
        """Triggers dynamic threat alerts on Dashboard and Sidebar."""
        self.update_global_threat_level(88)

    def _on_attack_restored(self):
        """Resets threat alerts and sets system status back to protected across all panels."""
        if hasattr(self.defense, 'reset_defense_alarm'):
            self.defense.reset_defense_alarm()
        self.update_global_threat_level(0)

    def _release_topmost_lock(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()
        self.activateWindow()

    def resizeEvent(self, event):
        if hasattr(self, 'overlay'):
            self.overlay.move(self.width() - 330, self.height() - 130)
        super().resizeEvent(event)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("SideBar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(10)

        brand_card = QFrame()
        brand_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0a1838, stop:1 #030816);
                border: 1px solid #102a5c;
                border-radius: 10px;
            }
        """)
        b_layout = QVBoxLayout(brand_card)
        b_layout.setContentsMargins(12, 12, 12, 12)
        b_layout.setSpacing(4)
        b_layout.setAlignment(Qt.AlignCenter)

        title_row = QHBoxLayout()
        title_row.setAlignment(Qt.AlignCenter)
        title_row.setSpacing(8)

        shield_icon = QLabel("🛡️")
        shield_icon.setStyleSheet("font-size: 20px; border: none; background: transparent;")

        self.title_lbl = QLabel()
        self.title_lbl.setTextFormat(Qt.RichText)
        self.title_lbl.setText("<span style='color:#ffffff; font-size:18px; font-weight:900;'>Crypto</span><span style='color:#00d2ff; font-size:18px; font-weight:900;'>Guard</span>")
        self.title_lbl.setStyleSheet("border: none; background: transparent;")

        title_row.addWidget(shield_icon)
        title_row.addWidget(self.title_lbl)

        sub_lbl = QLabel("Ransomware Detection & EDR")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setStyleSheet("""
            color: #38bdf8; 
            font-size: 10px; 
            font-weight: 700; 
            letter-spacing: 0.4px;
            border: none;
            background: transparent;
        """)

        self.signal_lbl = QLabel(self.signal_frames[0])
        self.signal_lbl.setAlignment(Qt.AlignCenter)
        self.signal_lbl.setStyleSheet("""
            color: #00d2ff; 
            font-size: 9px; 
            font-weight: 700; 
            font-family: 'Consolas', monospace;
            border: none;
            background: transparent;
            margin-top: 2px;
        """)

        b_layout.addLayout(title_row)
        b_layout.addWidget(sub_lbl)
        b_layout.addWidget(self.signal_lbl)

        layout.addWidget(brand_card)

        user_info = QFrame()
        user_info.setObjectName("UserProfileCard")
        user_layout = QVBoxLayout(user_info)
        user_layout.setContentsMargins(12, 10, 12, 10)
        user_layout.setSpacing(8)

        user_rbac = self.core.get('rbac')
        name = user_rbac.current_user if user_rbac else "AdminUser"
        role = user_rbac.current_role if user_rbac else "ADMIN"

        user_row = QHBoxLayout()
        user_row.setSpacing(10)

        avatar = QLabel("👤")
        avatar.setStyleSheet("background-color: #1e293b; border-radius: 12px; font-size: 11px; border: 1px solid #334155;")
        avatar.setFixedSize(26, 26)
        avatar.setAlignment(Qt.AlignCenter)

        user_lbl = QLabel(name)
        user_lbl.setStyleSheet("font-weight: 800; color: #ffffff; font-size: 13px; border: none;")

        user_row.addWidget(avatar)
        user_row.addWidget(user_lbl)
        user_row.addStretch()
        user_layout.addLayout(user_row)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(6)

        role_badge = QLabel(f"ROLE: {role}")
        role_badge.setStyleSheet("""
            color: #38bdf8;
            font-size: 9px;
            font-weight: 800;
            background-color: rgba(2, 132, 199, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 4px;
            padding: 2px 6px;
        """)

        status_lbl = QLabel("● ONLINE")
        status_lbl.setStyleSheet("color: #10b981; font-size: 9px; font-weight: 800; border: none;")

        meta_row.addWidget(role_badge)
        meta_row.addStretch()
        meta_row.addWidget(status_lbl)
        user_layout.addLayout(meta_row)

        layout.addWidget(user_info)

        self.nav_buttons = []
        nav_items = [
            ("📊  Dashboard", 0),
            ("🧪  Simulation", 1),
            ("🛡️  Defense Center", 2),
            ("📝  Reports & Ops", 3),
            ("🎮  Cyber Range", 4),
            ("🔑  Key Vault", 5),
            ("🔬  Forensic Lab", 6),
        ]

        nav_container = QVBoxLayout()
        nav_container.setSpacing(2)

        for text, index in nav_items:
            btn = self.create_nav_btn(text, index)
            nav_container.addWidget(btn)
            self.nav_buttons.append(btn)

        layout.addLayout(nav_container)

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        status_card = QFrame()
        status_card.setObjectName("SystemStatusCard")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(12, 10, 12, 10)
        status_layout.setSpacing(4)

        sec_title = QLabel("SYSTEM STATUS")
        sec_title.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; border: none;")

        state_row = QHBoxLayout()
        state_icon = QLabel("🛡️")
        state_icon.setStyleSheet("font-size: 12px; border: none;")
        
        self.state_txt = QLabel("Protected")
        self.state_txt.setStyleSheet("color: #10b981; font-size: 13px; font-weight: 800; border: none;")
        
        state_row.addWidget(state_icon)
        state_row.addWidget(self.state_txt)
        state_row.addStretch()

        self.lbl_uptime = QLabel("Uptime: 0d 0h 0m 0s")
        self.lbl_uptime.setStyleSheet("color: #00d2ff; font-size: 11px; font-weight: 600; border: none;")

        self.lbl_last_scan = QLabel("Last Scan: Syncing...")
        self.lbl_last_scan.setStyleSheet("color: #64748b; font-size: 10px; border: none;")

        status_layout.addWidget(sec_title)
        status_layout.addLayout(state_row)
        status_layout.addWidget(self.lbl_uptime)
        status_layout.addWidget(self.lbl_last_scan)

        layout.addWidget(status_card)

        sidebar.setLayout(layout)
        return sidebar

    def create_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setObjectName("NavBtn")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self.switch_tab(index, btn))
        return btn

    def switch_tab(self, index, active_btn):
        self.content_stack.setCurrentIndex(index)
        for btn in self.nav_buttons:
            btn.setChecked(btn == active_btn)

    def update_realtime_telemetry(self):
        elapsed = int(time.time() - self.start_time)
        
        self.signal_idx = (self.signal_idx + 1) % len(self.signal_frames)
        if hasattr(self, 'signal_lbl'):
            self.signal_lbl.setText(self.signal_frames[self.signal_idx])

        days = elapsed // 86400
        hours = (elapsed % 86400) // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60

        self.lbl_uptime.setText(f"Uptime: {days}d {hours}h {mins}m {secs:02d}s")

        now_str = datetime.now().strftime("%d %b %Y, %H:%M:%S")
        self.lbl_last_scan.setText(f"Last Scan: {now_str}")